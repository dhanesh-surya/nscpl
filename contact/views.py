from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from .forms import ContactForm
from .models import ContactInfo, ContactMessage


class ContactView(TemplateView):
    template_name = 'contact/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get active contact information
        try:
            contact_info = ContactInfo.objects.filter(is_active=True).first()
            if not contact_info:
                # Create default contact info if none exists
                contact_info = ContactInfo.objects.create(
                    company_name="NSCPL PRIVATE LIMITED",
                    address_line_1="123 Sports Avenue",
                    city="City",
                    state="State",
                    postal_code="12345",
                    country="India",
                    primary_phone="+1 (555) 123-4567",
                    primary_email="info@nscpl.com"
                )
        except Exception:
            contact_info = None
        
        context.update({
            'form': ContactForm(),
            'contact_info': contact_info,
            'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        })
        return context
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        
        if form.is_valid():
            try:
                # Save the contact message to database
                contact_message = form.save()
                
                # Get contact info for email
                contact_info = ContactInfo.objects.filter(is_active=True).first()
                
                # Send email notification
                if contact_info and settings.EMAIL_HOST_USER:
                    try:
                        send_mail(
                            subject=f'New Contact Form Submission: {contact_message.subject}',
                            message=f'''
New contact form submission received:

Name: {contact_message.name}
Email: {contact_message.email}
Phone: {contact_message.phone or 'Not provided'}
Subject: {contact_message.subject}

Message:
{contact_message.message}

---
Submitted on: {contact_message.created_at}
Message ID: {contact_message.id}
                            ''',
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[contact_info.primary_email],
                            fail_silently=False,
                        )
                    except Exception as email_error:
                        # Log email error but don't fail the form submission
                        print(f"Email sending failed: {email_error}")
                
                messages.success(
                    request, 
                    'Thank you for your message! We have received your inquiry and will get back to you within 24 hours.'
                )
                return redirect('contact:contact')
                
            except Exception as e:
                messages.error(
                    request, 
                    'Sorry, there was an error processing your message. Please try again or contact us directly.'
                )
        else:
            messages.error(
                request, 
                'Please correct the errors below and try again.'
            )
        
        context = self.get_context_data()
        context['form'] = form
        context['GOOGLE_MAPS_API_KEY'] = settings.GOOGLE_MAPS_API_KEY
        return render(request, self.template_name, context)


@method_decorator(csrf_exempt, name='dispatch')
class ContactAjaxView(TemplateView):
    """AJAX endpoint for contact form submissions"""
    
    def post(self, request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Invalid request'}, status=400)
        
        form = ContactForm(request.POST)
        
        if form.is_valid():
            try:
                contact_message = form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you for your message! We will get back to you soon.',
                    'message_id': contact_message.id
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': 'Failed to save message. Please try again.'
                }, status=500)
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)


def get_contact_info(request):
    """API endpoint to get contact information"""
    try:
        contact_info = ContactInfo.objects.filter(is_active=True).first()
        if contact_info:
            return JsonResponse({
                'success': True,
                'data': {
                    'company_name': contact_info.company_name,
                    'address': contact_info.get_full_address(),
                    'phone': contact_info.primary_phone,
                    'email': contact_info.primary_email,
                    'business_hours': {
                        'weekdays': contact_info.business_hours_weekdays,
                        'saturday': contact_info.business_hours_saturday,
                        'sunday': contact_info.business_hours_sunday,
                    },
                    'social_links': contact_info.get_social_links(),
                    'map_settings': {
                        'latitude': float(contact_info.latitude) if contact_info.latitude else None,
                        'longitude': float(contact_info.longitude) if contact_info.longitude else None,
                        'zoom': contact_info.map_zoom,
                        'show_map': contact_info.show_map,
                    }
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'No contact information available'
            }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Failed to retrieve contact information'
        }, status=500)
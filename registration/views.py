from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import PlayerRegistrationForm, CustomPlayerRegistrationForm
from .models import PlayerRegistration
from core.models import WebsiteTheme
from .models import RegistrationPageSetting

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER

def register_player(request):
    if request.method == 'POST':
        form = CustomPlayerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            player = form.save()
            return redirect('registration_success', player_id=player.id)  # Redirect to a success page with player_id
    else:
        form = CustomPlayerRegistrationForm()

    payment_info = {
        'bank': 'State Bank of India',
        'account_number': '44477347602',
        'ifsc_code': 'SBIN0003740',
    }

    context = {
        'form': form,
        'payment_info': payment_info,
        'theme': WebsiteTheme.objects.filter(is_active=True).first(),
        'registration_style': RegistrationPageSetting.objects.filter(is_active=True).first()
    }
    return render(request, 'registration/registration_form.html', context)

def registration_success(request, player_id):
    return render(request, 'registration/registration_success.html', {'player_id': player_id})

def generate_player_pdf(request, player_id):
    player = get_object_or_404(PlayerRegistration, pk=player_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="registration_form_{player.first_name}_{player.sur_name}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom Styles for Header and Instructions
    header_style_red = ParagraphStyle('HeaderRed', parent=styles['h1'], alignment=TA_CENTER, fontSize=20, textColor='#FF0000', spaceAfter=6)
    header_style_blue = ParagraphStyle('HeaderBlue', parent=styles['h2'], alignment=TA_CENTER, fontSize=14, textColor='#0000FF', spaceAfter=4)
    instruction_style = ParagraphStyle('Instruction', parent=styles['Normal'], fontSize=10, leading=12, spaceBefore=6)

    # Header Information
    story.append(Paragraph("NSCPL Pvt. Ltd. Open Trials For Players", header_style_red))
    story.append(Paragraph("(conduct by New Series Cricket Premier leagues)", header_style_blue))
    story.append(Paragraph("Organized by NSCPL Chhattisgarh", header_style_blue))
    story.append(Paragraph("Application Form for Player Registration", header_style_blue))
    story.append(Spacer(1, 0.2 * inch))

    # Venue and Date Placeholders
    story.append(Paragraph(f"<b>Venue :</b> {player.venue} <b>Date :</b> {player.date_of_event}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Instructions
    story.append(Paragraph("<b>Instructions:</b>", styles['h3']))
    story.append(Paragraph("1. The organizers have entire right to cancel /postpone the event for reasons not required to be made public. No candidate Shall challenge the decision in this regard.", instruction_style))
    story.append(Paragraph("2. Only the boys born from 01/01 2011 are eligible for the trials.", instruction_style))
    story.append(Paragraph("3. Players who have attended similar hold earlier.", instruction_style))
    story.append(Paragraph("4. Players should not carry any cricket with them while reporting for the trials organizer will not be responsible for safeguarding of personal belonging.", instruction_style))
    story.append(Paragraph("5. It is compulsory to wear T shirt + Touser + sport shoes", instruction_style))
    story.append(Paragraph("6. This registration form should be submitted at the registration in the camp", instruction_style))
    story.append(Spacer(1, 0.4 * inch))

    # Title
    title_style = ParagraphStyle('Title', parent=styles['h1'], alignment=TA_CENTER, fontSize=24, spaceAfter=12)
    story.append(Paragraph("Player Registration Form", title_style))
    story.append(Spacer(1, 0.2 * inch))

    # Player Photo
    if player.photo:
        try:
            img_path = player.photo.path
            img = Image(img_path, width=1.5*inch, height=1.5*inch)
            story.append(img)
            story.append(Spacer(1, 0.2 * inch))
        except FileNotFoundError:
            story.append(Paragraph("Player photo not found.", styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))

    # Personal Information
    story.append(Paragraph("<b>Personal Information</b>", styles['h2']))
    story.append(Paragraph(f"<b>Surname:</b> {player.sur_name}", styles['Normal']))
    story.append(Paragraph(f"<b>First Name:</b> {player.first_name}", styles['Normal']))
    story.append(Paragraph(f"<b>Father's Name:</b> {player.fathers_name}", styles['Normal']))
    story.append(Paragraph(f"<b>Date of Birth:</b> {player.date_of_birth}", styles['Normal']))
    story.append(Paragraph(f"<b>Gender:</b> {player.gender}", styles['Normal']))
    story.append(Paragraph(f"<b>Address:</b> {player.address}, {player.city}, {player.state}, {player.zip_code}, {player.country}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Contact Information
    story.append(Paragraph("<b>Contact Information</b>", styles['h2']))
    story.append(Paragraph(f"<b>Email:</b> {player.email}", styles['Normal']))
    story.append(Paragraph(f"<b>Phone Number:</b> {player.phone_number}", styles['Normal']))
    story.append(Paragraph(f"<b>WhatsApp Number:</b> {player.whatsapp_number if player.whatsapp_number else 'N/A'}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Playing Information
    story.append(Paragraph("<b>Playing Information</b>", styles['h2']))
    story.append(Paragraph(f"<b>Primary Playing Role:</b> {player.primary_playing_role}", styles['Normal']))
    story.append(Paragraph(f"<b>Secondary Playing Role:</b> {player.secondary_playing_role if player.secondary_playing_role else 'N/A'}", styles['Normal']))
    story.append(Paragraph(f"<b>Faster Bowler:</b> {player.faster_bowler if player.faster_bowler else 'N/A'}", styles['Normal']))
    story.append(Paragraph(f"<b>Spin Bowler:</b> {player.spin_bowler if player.spin_bowler else 'N/A'}", styles['Normal']))
    story.append(Paragraph(f"<b>Batting Proficiency:</b> {player.batting_proficiency if player.batting_proficiency else 'N/A'}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Declarations
    story.append(Paragraph("<b>Declarations</b>", styles['h2']))
    story.append(Paragraph(f"<b>Physically Fit:</b> {'Yes' if player.physically_fit else 'No'}", styles['Normal']))
    story.append(Paragraph(f"<b>Past Tournament Declaration:</b> {'Agreed' if player.declaration_past_tournament else 'Not Agreed'}", styles['Normal']))
    story.append(Paragraph(f"<b>Parents Aware Declaration:</b> {'Agreed' if player.declaration_parents_aware else 'Not Agreed'}", styles['Normal']))
    story.append(Paragraph(f"<b>Indemnify Organizers Declaration:</b> {'Agreed' if player.declaration_indemnify_organizers else 'Not Agreed'}", styles['Normal']))
    story.append(Paragraph(f"<b>Emergency Care Declaration:</b> {'Agreed' if player.declaration_emergency_care else 'Not Agreed'}", styles['Normal']))
    story.append(Paragraph(f"<b>Photo/Video Consent:</b> {'Agreed' if player.declaration_photo_video_consent else 'Not Agreed'}", styles['Normal']))
    story.append(Paragraph(f"<b>True Info Declaration:</b> {'Agreed' if player.declaration_true_info else 'Not Agreed'}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Payment Information
    story.append(Paragraph("<b>Payment Information</b>", styles['h2']))
    story.append(Paragraph(f"<b>Transaction ID:</b> {player.transaction_id if player.transaction_id else 'N/A'}", styles['Normal']))
    if player.transaction_screenshot:
        story.append(Paragraph("<b>Transaction Screenshot:</b> Attached", styles['Normal']))
    else:
        story.append(Paragraph("<b>Transaction Screenshot:</b> Not Provided", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph(f"<b>Registration Date:</b> {player.registration_date.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))

    doc.build(story)
    return response

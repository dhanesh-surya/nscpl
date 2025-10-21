from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.ContactView.as_view(), name='contact'),
    path('ajax/', views.ContactAjaxView.as_view(), name='contact_ajax'),
    path('api/contact-info/', views.get_contact_info, name='contact_info_api'),
]

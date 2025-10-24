from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_player, name='register_player'),
    path('register/success/<int:player_id>/', views.registration_success, name='registration_success'),
    path('register/pdf/<int:player_id>/', views.generate_player_pdf, name='generate_player_pdf'),
]
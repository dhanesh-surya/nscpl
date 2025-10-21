from django.urls import path
from . import views

app_name = 'sports'

urlpatterns = [
    path('', views.SportListView.as_view(), name='sport_list'),
    path('<slug:slug>/', views.SportDetailView.as_view(), name='sport_detail'),
    path('<slug:slug>/edit/', views.SportUpdateView.as_view(), name='sport_update'),
]

from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('upcoming-events/', views.UpcomingEventsView.as_view(), name='upcoming_events'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
]

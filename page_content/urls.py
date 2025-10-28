from django.urls import path
from . import views

app_name = 'page_content'

urlpatterns = [
    path('', views.page_detail, name='page_detail'),
]
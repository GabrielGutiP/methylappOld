from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
]
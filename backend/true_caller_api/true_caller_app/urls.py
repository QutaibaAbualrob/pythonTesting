from django.urls import path

from . import views

urlpatterns = [
    path('phonenames/', views.phonenames, name='phonenames'),
    
]

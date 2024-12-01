from django.urls import path
from . import views

from django.urls import path, include

urlpatterns = [
    path('hello/', views.say_hello),
    path('upload_pdf/', views.upload_pdf)
]
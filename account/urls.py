from django.urls import path

from .views import *

urlpatterns = [
    path('sing-up/', RegisterView.as_view(), name='register'),
    path('login/', SignInView.as_view(), name='login')
]
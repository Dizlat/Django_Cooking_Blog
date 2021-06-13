from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .models import User
from  .forms import RegistrationForm


class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'account/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')
    success_message = 'Successfully registered!'


class SignInView(LoginView):
    template_name = 'account/login.html'


def profile(request):
    return render(request, 'account/profile.html')


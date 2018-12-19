# coding: utf-8
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.forms import UserCreationForm


class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('app:signin')
    template_name = 'app/signup.html'

from django.shortcuts import render
from django.views.generic import TemplateView

class HomeClass(TemplateView):
    template_name = 'home.html'

from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class Index_view(TemplateView):
    template_name='website/index_view.html'

class Contact_view(TemplateView):
    template_name='website/contact_view.html'

class About_view(TemplateView):
    template_name='website/about_view.html'
    
    
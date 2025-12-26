from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def phonenames(request):
    template = loader.get_template('first.html')
    return HttpResponse(template.render())
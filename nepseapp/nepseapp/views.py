from .models import *
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

# Create your views here.
def home(request):
    return render(request, 'nepse/home.html')

def about(request):
    return render(request, 'nepse/about.html')

def contact(request):
    return render(request, 'nepse/contact.html')

def index(request):
    return render(request, 'nepse/index.html')


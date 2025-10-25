from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
# Create your views here.

def home(request):
    template_name = 'guest/parciales/home.html'
    
    return render(request,template_name)

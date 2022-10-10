from django.shortcuts import render
from django.http import HttpResponse

from .models import Film

# Create your views here.

def home(request):
    zoekTerm = request.GET.get('zoekFilm')
    if zoekTerm:
        films = Film.objects.filter(titel_contains=zoekTerm)
    else:
        films = Film.objects.all()
    #films = Film.objects.all()
    return render(request, 'home.html', {'zoekTerm':zoekTerm, 'films':films})

def over(request):
    return HttpResponse('<h1>Welkom op de over-ons</h1>')

def schrijfin(request):
    email = request.GET.get('email')
    return render(request, 'schrijfin.html', {'email':email})
    
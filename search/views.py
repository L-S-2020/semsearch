from django.shortcuts import render
import requests

# Create your views here.
def search(request, term):
    boogle = requests.get('https://boogle.boreal.express/search?q=' + term)
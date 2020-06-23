from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def home_view(request):
    return HttpResponse('Nc19 Proxy home!')
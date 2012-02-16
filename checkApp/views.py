# Create your views here.
from django.shortcuts import render, get_object_or_404

def index(request):
    return render(request, 'checkApp/index.html')
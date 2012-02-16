# Create your views here.
from django.shortcuts import render, get_object_or_404
from checkApp.models import CheckList,CheckItem

def index(request):
    clist = CheckList.objects.all()
    context = {
        'list': clist,
    }
    return render(request, 'checkApp/index.html', context)
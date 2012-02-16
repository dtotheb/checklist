# Create your views here.
from django.shortcuts import render, get_object_or_404
from checkApp.models import CheckList, CheckItem


def index(request):
    clist = CheckList.objects.all()
    context = {
        'list': clist,
    }
    return render(request, 'checkApp/index.html', context)


def viewList(request, pk):
    list = get_object_or_404(CheckList, pk=pk)
    context = {
        'list': list
    }
    return render(request, 'checkApp/viewList.html', context)

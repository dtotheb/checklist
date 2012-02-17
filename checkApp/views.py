# Create your views here.
from django.shortcuts import render, get_object_or_404
from checkApp.models import CheckList, CheckItem
from django.core.context_processors import csrf
from django.http import Http404, HttpResponse
from django.core import serializers


def index(request):
    clist = CheckList.objects.all()
    context = {
        'list': clist,
        'title': 'yay'
    }
    return render(request, 'checkApp/index.html', context)


def viewList(request, pk):
    list = get_object_or_404(CheckList, pk=pk)
    context = {
        'list': list,
        'title': list.name,
        'csrf': csrf(request)
    }
    return render(request, 'checkApp/viewList.html', context)

def checkItemDone(request):
    if request.is_ajax() and request.method =="POST":
        pk = request.POST['pk']
        val = request.POST['val']
        try:
            CI = CheckItem.objects.get(pk=pk)
        except CheckItem.DoesNotExist:
            return Http404

        if val == 'true':
            CI.done = False
        else:
            CI.done = True

        CI.save()
        data = serializers.serialize('json',[CI])
        return HttpResponse(data)
    else:
        return HttpResponse(status=405)








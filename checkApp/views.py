# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.core.context_processors import csrf
from django.http import Http404, HttpResponse
from django.core import serializers

from checkApp.models import CheckList, Task
from checkApp.forms import TaskForm


def index(request):
    clist = CheckList.objects.all()
    context = {
        'list': clist,
        'title': 'yay'
    }
    return render(request, 'checkApp/index.html', context)


def viewList(request, pk):
    list = get_object_or_404(CheckList, pk=pk)
    form = TaskForm()
    context = {
        'list': list,
        'title': list.name,
        'csrf': csrf(request),
        'form':form
    }
    return render(request, 'checkApp/viewList.html', context)

def taskDone(request):
    if request.is_ajax() and request.method == "POST":
        pk = request.POST['pk']
        val = request.POST['val']
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Http404

        if val == 'true':
            task.done = False
        else:
            task.done = True

        task.save()
        data = serializers.serialize('json',[task])
        return HttpResponse(data)
    else:
        return HttpResponse(status=403)

def createTask(request):
    if request.is_ajax() and request.method == "POST":
        pk = request.POST['pk']
        try:
            list = CheckList.objects.get(pk=pk)
        except CheckList.DoesNotExist:
            return Http404

        item = Task.objects.create(
            checkList = list,
            text = request.POST['text'],
            done = False
        )

        item.save()
        data = serializers.serialize('json',[item])
        return HttpResponse(data)
    else:
        return HttpResponse(status=403)









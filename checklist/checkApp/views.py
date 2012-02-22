# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.core import serializers

from checkApp.models import CheckList, Task, Template
from checkApp.forms import TaskForm, CheckListForm


def index(request):
    """
    Index view with:
    List of Checklists
    Form for Inserting a New checklist
    """
    clist = CheckList.objects.all()
    if request.user.username:
        username = request.user.username
    else:
        username = 'anon'
    form = CheckListForm(initial={'creator': username})
    context = {
        'list': clist,
        'title': 'Checklists',
        'form': form
    }
    return render(request, 'checkApp/index.html', context)


def viewList(request, pk):
    """
    viewList of CheckList Details with:
    List of Tasks for a Checklist
    Form for inserting new tasks
    """
    list = get_object_or_404(CheckList, pk=pk)
    form = TaskForm(initial={'checkList': list})
    tasks = list.tasks.all()
    context = {
        'list': list,
        'title': list.name,
        'tasks': tasks,
        'form': form
    }
    return render(request, 'checkApp/viewList.html', context)


def taskDone(request):
    """
    Ajax view for updating a Task's done status
    Accepts a post request with:
        pk = Pk of the Task being updated
        val = The new state of done, either true or false
    Returns JSON:
    [{"pk": 1,
      "model": "checkApp.task",
      "fields": {"text": "test this",
                 "done": false,
                 "checkList": 1}}]
    """
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
        data = serializers.serialize('json', [task])
        return HttpResponse(data)
    else:
        return HttpResponse(status=403)


def createTask(request):
    """
    Ajax View for Handling Form submits when Creating new Tasks
    Accepts:
        TaskForm
    Returns JSON:
        [{"pk": 3,
        "model": "checkApp.task",
        "fields": {"text": "test",
                   "done": false,
                   "checkList": 1}}]
    """
    if request.is_ajax() and request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            item = form.save()
            data = serializers.serialize('json', [item])
            return HttpResponse(data)
        else:
            return HttpResponse(status=405)
    else:
        return HttpResponse(status=403)


def createCheckList(request):
    """
    Ajax view for handling Form submits when creating new Checklists
    Accepts:
        CheckListForm
    Returns JSON:
        [{"pk": 2,
         "model": "checkApp.checklist",
         "fields": {"name": "testlist",
                    "creator": "tester"}}]
    """
    if request.is_ajax() and request.method == "POST":
        form = CheckListForm(request.POST)
        if form.is_valid():
            list = form.save()
            data = serializers.serialize('json', [list])
            return HttpResponse(data)
    else:
        return HttpResponse(status=403)


def deleteCheckList(request):
    """
    Ajax View for Deleting a checklist and all the associated tasks
    """

    if request.is_ajax() and request.method == "POST":
        pk = request.POST['pk']
        list = get_object_or_404(CheckList, pk=pk)
        tasks = list.tasks.all()

        tasks.delete()
        list.delete()
        return HttpResponse(200)
    else:
        return HttpResponse(403)


def viewTemplates(request):
    """
    Lists all the available CheckList Templates
    """
    templates = Template.objects.all()

    context = {
        'templates': templates,
        'title': 'Templates',
        }
    return render(request, 'checkApp/viewTemplates.html', context)


def startCheckList(request):
    """
    View for creating a new CheckList based on an existing template
    """
    pk = request.POST['pk']
    temp = get_object_or_404(Template, pk=pk)
    new_check = CheckList().createFromTemplate(temp, request.user.username)
    return redirect('viewList', new_check.pk)

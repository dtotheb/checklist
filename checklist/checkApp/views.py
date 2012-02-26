from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from checkApp.models import CheckList, Task, Template
from checkApp.forms import TaskForm, CheckListForm, LoginForm


def index(request):
    """
    Index view with:
    List of Checklists
    Form for Inserting a New checklist
    """

    if request.user.is_authenticated():
        username = request.user.username
        try:
            clist = CheckList.objects.filter(creator=username)
        except CheckList.DoesNotExist:
            clist = []
    else:
        username = 'anon'
        clist = CheckList.objects.all()

    form = CheckListForm(initial={'creator': username})

    context = {
        'list': clist,
        'title': 'Checklists',
        'form': form
    }
    return render(request, 'checkApp/index.html', context)


def login_view(request):
    """
    Login View
    """
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse(status=403)
        else:
            return HttpResponse(status=403)
    else:
        context = {
            'form': form
        }
        return render(request, 'checkApp/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')


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
        task = get_object_or_404(Task, pk=pk)

        if val == 'true':
            task.done = False
        else:
            task.done = True

        task.save()
        data = serializers.serialize('json', [task])
        return HttpResponse(data)
    else:
        return HttpResponse(status=403)


@login_required()
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


@login_required()
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


@login_required()
def deleteCheckList(request):
    """
    Ajax View for Deleting a checklist and all the associated tasks
    """

    if request.is_ajax() and request.method == "POST":
        pk = request.POST['pk']
        list = get_object_or_404(CheckList, pk=pk)
        if list.creator == request.user.username:
            tasks = list.tasks.all()
            tasks.delete()
            list.delete()
            data = '{"pk": ' + pk + '}'
            return HttpResponse(data)
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=405)


def viewTemplates(request):
    """
    Lists all the available CheckList Templates
    """
    templates = Template.objects.all()
    lists = CheckList.objects.all()
    context = {
        'templates': templates,
        'lists': lists,
        'title': 'Templates',
        }
    return render(request, 'checkApp/viewTemplates.html', context)


@login_required()
def startCheckList(request):
    """
    View for creating a new CheckList based on an existing template
    """
    pk = request.POST['pk']
    temp = get_object_or_404(Template, pk=pk)
    new_check = CheckList().createFromTemplate(temp, request.user.username)
    return redirect('viewList', new_check.pk)


@login_required()
def startTemplate(request):
    """
    View for creating a new Template based on an existing checklist
    """
    pk = request.POST['pk']
    check = get_object_or_404(CheckList, pk=pk)
    new_temp = Template().createFromCheckList(check)
    return redirect('viewTemplates')

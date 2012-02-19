from django import forms
from checkApp.models import CheckList, Task


class TaskForm(forms.ModelForm):
    """
    ModelForm for creating Tasks
    """
    class Meta:
        model = Task
        exclude = ('done', )
        widgets = {
            'checkList': forms.HiddenInput(),
        }


class CheckListForm(forms.ModelForm):
    """
    ModelForm for Creating Checklists
    """
    class Meta:
        model = CheckList

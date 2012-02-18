from django import forms
from checkApp.models import CheckList, Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('done', )
        widgets = {
            'checkList': forms.HiddenInput(),
        }


class CheckListForm(forms.ModelForm):
    class Meta:
        model = CheckList

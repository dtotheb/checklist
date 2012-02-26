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
        widgets = {
            'creator': forms.HiddenInput(),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField()

    class Meta:
        widgets = {
            'password': forms.PasswordInput(),
        }

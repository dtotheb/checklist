from django import forms
from checkApp.models import CheckList


class TaskForm(forms.Form):
    text = forms.CharField(max_length=100)
    pk = forms.IntegerField()


class CheckListForm(forms.ModelForm):
    class Meta:
        model = CheckList
    name = forms.CharField(max_length=100)
    creator = forms.CharField(max_length=100)

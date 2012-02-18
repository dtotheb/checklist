from django import forms


class TaskForm(forms.Form):
    text = forms.CharField(max_length=100)
    pk = forms.IntegerField()


class CheckListForm(forms.Form):
    name = forms.CharField(max_length=100)
    creator = forms.CharField(max_length=100)

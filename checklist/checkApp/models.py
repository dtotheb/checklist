from django.db import models


class CheckList(models.Model):
    name = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Task(models.Model):
    text = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    checkList = models.ForeignKey(CheckList, related_name='tasks')

    def __unicode__(self):
        return self.text

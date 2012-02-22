from django.db import models
from picklefield import PickledObjectField


class CheckList(models.Model):
    """
    Model for representing the CheckList
    """
    name = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Task(models.Model):
    """
    Model for Representing a Task in a CheckList
    """
    text = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    checkList = models.ForeignKey(CheckList, related_name='tasks')

    def __unicode__(self):
        return self.text


class Template(models.Model):
    """
    Template Model based on the CheckList
    Expect it stores the tasks in a PickleField instead of a related_name
    """
    name = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)
    pickledTasks = PickledObjectField(null=True)

    def createFromCheckList(self, checkList):
        """
        Mirrors a CheckList's data and tasks into the Template
        Grabs the Templates tasks and stick them in a pickleField
        """
        self.name = checkList.name
        self.creator = checkList.creator
        self.pickledTasks = checkList.tasks.all()
        self.save()

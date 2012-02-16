from django.db import models

# Create your models here.
class CheckList(models.Model):
    name = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class CheckItem(models.Model):
    text = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    checkList = models.ForeignKey(CheckList,related_name='items')

    def __unicode__(self):
        return self.text
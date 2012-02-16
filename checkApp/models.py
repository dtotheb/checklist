from django.db import models

# Create your models here.
class CheckList(models.Model):
    name = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

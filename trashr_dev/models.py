from django.db import models

class Dumpster(models.Model):
    percent_capacity = models.IntegerField(default=0)

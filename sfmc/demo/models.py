from __future__ import unicode_literals

from django.db import models

class Log(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    jwt = models.TextField(default='')

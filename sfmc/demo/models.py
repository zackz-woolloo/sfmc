from __future__ import unicode_literals

from django.db import models

class Log(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    jwt = models.TextField(default='')


class AccessToken(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    access_token = models.TextField(default='')
    refresh_token = models.TextField(default='')
    expires_in = models.PositiveIntegerField(default=0)
    auth_url = models.TextField(default='')

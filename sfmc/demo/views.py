from rest_framework.views import APIView
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import View
from .models import Log

class SignInView(APIView):

    def post(self, request, *args, **kwargs):
        jwt = request.POST.get('JWT')

        Log.objects.create(jwt=jwt)

        # use lib from https://github.com/jpadilla/pyjwt to decode 
        return Response('Done')



class LogView(View):
    def get(self, request, format=None):
        logs = Log.objects.all()
        return render(request, 'log.html', {'logs':logs})
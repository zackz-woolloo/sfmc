from rest_framework.views import APIView
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import View
from django.http import HttpResponse
from rest_framework.response import Response
from .models import Log, AccessToken, Event
import requests, json

app_sig = '4jl0ssf4wzjpk04gzc3ox3ihsbtyqybzmlslghdln42zktzdyvwnjocvh5cbddtju0r4y3yduohwfnsyh1opfyglac55b3swdswnhgy4broxalzpvvd3fzspo4rx2s3tyjdomccjd4x32zfjsxl3gmz0ktazysnhkoaroi3x4ysslkbwinxjscpnsthdmw2ig3bcejqs2l3mhxmx3vc1b1wwiu0aff0r4tenzgyz04aaos1xycgcqbbog42jea2'
client_id = '4a44m9ej6uw2w5vp2ip5p5b9'
client_secret = '7phHgkukdMJLERGQfgOOh5Jg'

class IndexView(View):
    def get(self, request, format=None):
        return render(request, 'index.html', {})

class ActivityActionView(APIView):
    def post(self, request, *args, **kwargs):
        print(kwargs.get('action'))
        print(request.POST)
        return Response({'ok':True})


class SignInView(APIView):

    def _parse_jwt(self, token):
        import jwt
        payload = jwt.decode(token, app_sig, algorithms=['HS256'])
        
        rest = payload['request']['rest']
        auth_url = rest['authEndpoint']
        refresh_token = rest['refreshToken']

        data = {
            'clientId':client_id, 
            'clientSecret':client_secret, 
            'refreshToken':refresh_token, 
            'accessType':'offline'
        }
        r = requests.post(auth_url, data=data)
        response = r.json()
        AccessToken.objects.all().delete()

        access_token = AccessToken.objects.create(
            access_token=response['accessToken'],
            refresh_token=response['refreshToken'],
            expires_in=response['expiresIn'],
            auth_url=auth_url
        )

        return payload, access_token

    def post(self, request, *args, **kwargs):
        token = request.POST.get('jwt')

        Log.objects.create(jwt=token)
        payload, access_token = self._parse_jwt(token)
        # use lib from https://github.com/jpadilla/pyjwt to decode 
        return HttpResponse('Done')

    def get(self, request, *args, **kwargs):
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0ODA5MTAyOTUsImp0aSI6InZEWWtrWkVVeVQ3LWZORVNDS0tZRURlc0dxOCIsInJlcXVlc3QiOnsiY2xhaW1zVmVyc2lvbiI6MiwidXNlciI6eyJpZCI6NzQ5MzM3MSwiZW1haWwiOiJhaWRhbmhAd29vbGxvby5jb20iLCJjdWx0dXJlIjoiZW4tVVMiLCJ0aW1lem9uZSI6eyJsb25nTmFtZSI6IihHTVQtMDY6MDApIENlbnRyYWwgVGltZSAoTm8gRGF5bGlnaHQgU2F2aW5nKSIsInNob3J0TmFtZSI6IkNTVCIsIm9mZnNldCI6LTYuMCwiZHN0IjpmYWxzZX19LCJyZXN0Ijp7ImF1dGhFbmRwb2ludCI6Imh0dHBzOi8vYXV0aC1zNy5leGFjdHRhcmdldGFwaXMuY29tL3YxL3JlcXVlc3RUb2tlbiIsImFwaUVuZHBvaW50QmFzZSI6Imh0dHBzOi8vd3d3LmV4YWN0dGFyZ2V0YXBpcy5jb20vIiwicmVmcmVzaFRva2VuIjoiN2xkem5ndVh1Y0lzeWJjSmEwSG5zOVo0In0sIm9yZ2FuaXphdGlvbiI6eyJpZCI6NzI4NzY3NCwiZW50ZXJwcmlzZUlkIjo3Mjg3Njc0LCJkYXRhQ29udGV4dCI6ImVudGVycHJpc2UiLCJzdGFja0tleSI6IlM3IiwicmVnaW9uIjoiTkExIn0sImFwcGxpY2F0aW9uIjp7ImlkIjoiMjdmYTg5N2QtZmYyZC00NmZlLTk0ZWEtZjk3YWE3MTVlZTIwIiwicGFja2FnZSI6ImNvbS53b29sbG9vLm1rdGdjbG91ZCIsInJlZGlyZWN0VXJsIjoiaHR0cHM6Ly9zZm1jLndvb2xsb28uY29tL3NmbWMvcmVkaXJlY3QvIiwiZmVhdHVyZXMiOnt9LCJ1c2VyUGVybWlzc2lvbnMiOltdfX19.Cc5fcVP6KJ7FWp2EW3-SM8xd1eNkqrVFqOXHFrZ65tE'
        payload, access_token = self._parse_jwt(token)
        return render(request, 'test.html', {'token':token, 'payload':json.dumps(payload), 'access_token':access_token})

class TokenContextView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        headers = {'Authorization':'Bearer ' + token}
        r = requests.get('https://www.exacttargetapis.com/platform/v1/tokenContext/', headers=headers)
        response = r.json()
        print(response)

        return Response(response)

class RefreshTokenView(View):
    def get(self, request, *args, **kwargs):
        access_token = AccessToken.objects.first()
        auth_url = access_token.auth_url
        data = {
            'clientId':client_id, 
            'clientSecret':client_secret, 
            'refreshToken':access_token.refresh_token, 
            'accessType':'offline'
        }
        r = requests.post(auth_url, data=data)
        response = r.json()
        access_token.access_token = response['accessToken']
        access_token.refresh_token = response['refreshToken']
        access_token.expires_in = response['expiresIn']
        access_token.save()
        return render(request, 'refresh_token.html', {'access_token':access_token})

class CreateContactView(APIView):
    def get(self, request, *args, **kwargs):
        data = [{
            'keys':{
                'subscriberUUID':'1234abcd'
            },
            'values':{
                'email':'user@company.com',
                'name':'Test User'
            }
            }
        ]
        access_token = AccessToken.objects.first()
        headers = {'Authorization':'Bearer ' + access_token.access_token}
        print(headers)
        print(data)
        r = requests.post('https://www.exacttargetapis.com/contacts/v1/contacts', headers=headers, data=data)
        response = r.json()
        print(response)
        return Response(response)

class InsertRowView(APIView):
    def get(self, request, *args, **kwargs):
        event = Event.objects.first()
        '''
        data = [
            {
                'keys':{
                    "subscriberUUID":'1234abcd'
                },
                'values': {
                    'email':'user@company.com',
                    'name':'Test User'
                }
            }
        ]
        '''
        data = []
        access_token = AccessToken.objects.first()
        headers = {'Authorization':'Bearer ' + access_token.access_token}
        r = requests.post('https://www.exacttargetapis.com/hub/v1/dataevents/dda895e5-37bc-e611-8a02-1402ec67ad30/rowset', headers=headers, data=data)
        response = r.json()
        return Response(response)

class CreateContactEventView(APIView):
    def get(self, request, *args, **kwargs):
        event = Event.objects.first()
        data = {
            'ContactKey':'1234abcd',
            'EventDefinitionKey':event.event_id,
            'Data':[
            {
                'key':'win',
                'name':'win',
                'id':'dda895e5-37bc-e611-8a02-1402ec67ad30',
                'items':[{
                    'values':[
                        {'name':'subscriberUUID', 'value':'1234abcd'},
                        {'name':'email', 'value':'user@company.com'},
                        {'name':'name', 'value':'Test User'}
                    ]
                }]
            }]
        }
        access_token = AccessToken.objects.first()
        headers = {'Authorization':'Bearer ' + access_token.access_token}
        r = requests.post('https://www.exacttargetapis.com/contacts/v1/contactEvents', headers=headers, data=data)
        response = r.json()
        print(response)
        return Response(response)

class FireEventView(APIView):
    def get(self, request, *args, **kwargs):
        event = Event.objects.first()
        data = {
            'ContactKey':'1234abcd',
            'EventDefinitionKey':event.event_id,
            'Data':{
                'subscriberUUID':'1234abcd',
                'email':'user@company.com',
                'name':'Test User'
            }
        }
        access_token = AccessToken.objects.first()
        headers = {'Authorization':'Bearer ' + access_token.access_token}
        r = requests.post('https://www.exacttargetapis.com/interaction/v1/events', headers=headers, data=data)
        response = r.json()
        response['event_id'] = event.event_id
        print(response)
        return Response(response)

class LogView(View):
    def get(self, request, format=None):
        logs = Log.objects.all()
        events = Event.objects.all()
        return render(request, 'log.html', {'logs':logs, 'events':events})

class EventSaveView(APIView):
    def post(self, request, *args, **kwargs):
        event_id = request.POST.get('event_id')
        Event.objects.all().delete()
        Event.objects.create(event_id=event_id)
        return Response({'ok':True})
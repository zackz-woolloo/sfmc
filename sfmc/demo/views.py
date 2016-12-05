from rest_framework.views import APIView
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import View
from django.http import HttpResponse
from .models import Log, AccessToken
import requests, json

app_sig = 'uoa2fnkmnsb4y0plxrtazqywryhgv0d4atzy0faseuftwzmjjahgpvjwmjlzr0flsfs2ekk3zh4q2wacywgv0omewxzburezudtadh4nkmdjnrxvkagx5dcscx2ywe3ozcico2otlgctkhoyr3qn131iozgyudo52hqcqqkuzdgnsylcasaa22kpj1pfqx0e2as1jyncnnouwfyyf5hhguboe4owwityzofhqobqa2fdcn1241loitpjeox3b2q'

class IndexView(View):
    def get(self, request, format=None):
        return HttpResponse('ok')

class SignInView(APIView):

    def _parse_jwt(self, token):
        import jwt
        payload = jwt.decode(token, app_sig, algorithms=['HS256'])
        
        rest = payload['request']['rest']
        auth_url = rest['authEndpoint']
        refresh_token = rest['refreshToken']

        data = {
            'clientId':'szx4b3jywxd8you65cq5wtaa', 
            'clientSecret':'q32JBWUJTLnO0AUazQOxl7Ry', 
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

class RefreshTokenView(APIView):
    def get(self, request, *args, **kwargs):
        access_token = AccessToken.objects.first()
        auth_url = access_token.auth_url
        data = {
            'clientId':'szx4b3jywxd8you65cq5wtaa', 
            'clientSecret':'q32JBWUJTLnO0AUazQOxl7Ry', 
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

class LogView(View):
    def get(self, request, format=None):
        logs = Log.objects.all()
        return render(request, 'log.html', {'logs':logs})
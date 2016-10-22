from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.core.mail import EmailMessage

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def home(request):
    email = EmailMessage('SpaceoutVR Account Activation', 'hey buddy, blah', to=['agustinabreu@gmail.com'])
    email.send()
    return JSONResponse(status=200, data={'coins':1203, 'name':'pepe'})

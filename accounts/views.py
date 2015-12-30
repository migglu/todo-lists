import sys
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import redirect
from django.http import HttpResponse


def persona_login(request):
    user = authenticate(assertion=request.POST["assertion"])
    if user is not None:
        login(request, user)
    return HttpResponse("OK")

import os
import logging

from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.conf import settings

from rest_framework import status

from backend.auth import token

logging.basicConfig(filename='/var/log/secsaas/token.log',
                    filemode='a',
                    format="%(asctime)s %(levelname)s pid:%(process)d "\
                           "%(funcName)s (%(filename)s:%(lineno)d) "\
                           "%(message)s",
                    level=logging.DEBUG)

def login_required(view):
    def wrap(request, *args, **kwargs):
        logging.info(request)
        if 'HTTP_AUTHORIZATION' in request.META:
            auth_token = request.META['HTTP_AUTHORIZATION']
          
            auth_status, username = token.validate_token(
                                        settings.SECRET_KEY,
                                        auth_token)
            if auth_status:
                request.username = username
                return view(request, *args, **kwargs)

        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    return wrap

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


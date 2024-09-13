from django.http import Http404
from django.http import HttpResponse
from django.utils.decorators import method_decorator

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import json
import logging

from demo_site import url_utils, settings
from backend.auth import ldap, token

logging.basicConfig(filename='/var/log/secsaas/webgui.log',
                    filemode='a',
                    format="%(asctime)s %(levelname)s pid:%(process)d "\
                           "%(funcName)s (%(filename)s:%(lineno)d) "\
                           "%(message)s",
                    level=logging.DEBUG)


class LoginApi(APIView):
    """
    Handler for Login api
    """
    parser_classes = [JSONParser]

    def post(self, request):
        # tenantId=self.kwargs['tenantId']
        tenantId=request.GET.get('tenantId',None)
        request_json = request.data
        username = request_json.get('username', None)
        password = request_json.get('password', None)
        client_ip = url_utils.get_client_ip(request)

        logging.info("Login attempt from %s from IP %s for tenantId=%s",
                     username, client_ip,tenantId)
        if not username or not password or not tenantId:
            return HttpResponse("Invalid user",
                                status=status.HTTP_400_BAD_REQUEST)

        authenticated, user_obj = ldap.ldap_user_login(tenantId, username, password)
        logging.info("qqqqqqqqqq ",user_obj)
        if not authenticated:
            logging.warning("Invalid login attempt for %s from IP %s",
                            username, client_ip)
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

        auth_token = token.create_auth_token(settings.SECRET_KEY, username, tenantId)
        logging.info("Verification Successful")
        resp_json = {
            'username': username,
            'auth_token': auth_token
        }

        return HttpResponse(json.dumps(resp_json),
                            content_type="application/json",
                            status=status.HTTP_200_OK)

class currentUserApi(APIView):
    parser_classes = [JSONParser]
    @method_decorator(url_utils.login_required, name='dispatch')
    def get(self, request):
        response = token.decode_token(settings.SECRET_KEY, request.META['HTTP_AUTHORIZATION'])
        resp_json={
            'username':response['username'],
            'tenantId':response['tenantId']
        }
        return HttpResponse(json.dumps(resp_json),
                            content_type="application/json",
                            status=status.HTTP_200_OK)


class LogoutApi(APIView):
    """
    Handler for Logout api
    """
    parser_classes = [JSONParser]

    @method_decorator(url_utils.login_required, name='dispatch')
    def post(self, request):
        return HttpResponse(status=status.HTTP_200_OK)


class RenewApi(APIView):
    """
    Handler for Renew api
    """
    parser_classes = [JSONParser]

    @method_decorator(url_utils.login_required, name='dispatch')
    def post(self, request):
        auth_token = token.create_auth_token(settings.SECRET_KEY,
                                             request.username)

        resp_json = {
            'username': request.username,
            'auth_token': auth_token
        }

        return HttpResponse(json.dumps(resp_json),
                            content_type="application/json",
                            status=status.HTTP_200_OK)

class RegisterApi(APIView):
    """
    Handler for Login api
    """
    parser_classes = [JSONParser]

    def post(self, request):
        logging.info("kk123fgfhgfh2")
        request_json = request.data
        logging.info(request_json)
        username = request_json.get('username', None)
        password = request_json.get('password', None)
        client_ip = url_utils.get_client_ip(request)

        logging.info("Login attempt from %s from IP %s",
                     username, client_ip)
        if not username or not password:
            return HttpResponse("Invalid user",
                                status=status.HTTP_400_BAD_REQUEST)

        authenticated, user_obj = ldap.ldap_user_login(username, password)
        if not authenticated:
            logging.warning("Invalid login attempt for %s from IP %s",
                            username, client_ip)
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

        auth_token = token.create_auth_token(settings.SECRET_KEY, username)

        resp_json = {
            'username': username,
            'auth_token': auth_token
        }

        return HttpResponse(json.dumps(resp_json),
                            content_type="application/json",
                            status=status.HTTP_200_OK)
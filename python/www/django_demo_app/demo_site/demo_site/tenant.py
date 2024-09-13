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
from backend.tenant import tenant_api
logging.basicConfig(filename='/var/log/secsaas/webgui.log',
                    filemode='a',
                    format="%(asctime)s %(levelname)s pid:%(process)d "
                           "%(funcName)s (%(filename)s:%(lineno)d) "
                           "%(message)s",
                    level=logging.DEBUG)


class RegisterApi(APIView):
    """
    Handler for register api
    """
    parser_classes = [JSONParser]

    def post(self, request):
        request_json = request.data
        logging.info(request_json)
        name=request_json.get('name', None)
        address=request_json.get('address', None)
        adUrl=request_json.get('adDomainUrl', None)
        email=request_json.get('email', None)
        baseDn=request_json.get('basedn', None)
        tenantId=tenant_api.create_tenant(name, address, adUrl, email, baseDn)
      
        resp_json = {
            'tenantId': tenantId,
            "tenantUrl":request.build_absolute_uri('/login?tenantId=')+tenantId
        }
        logging.info(resp_json)
        return HttpResponse(json.dumps(resp_json),
                            content_type="application/json",
                            status=status.HTTP_200_OK)


class TenantApi(APIView):
    parser_classes=[JSONParser]
    @method_decorator(url_utils.login_required, name='dispatch')
    def get(self,request,tenantId):
        row=tenant_api.get_tenant_details(tenantId)
        resp_json={
            'data':row
        }
        return HttpResponse(json.dumps(resp_json),
                            content_type="application/json",
                            status=status.HTTP_200_OK)

class DeleteTenantApi(APIView):
    parser_classes=[JSONParser]
    @method_decorator(url_utils.login_required, name='dispatch')
    def delete(self, request,tenantId):
        msg=tenant_api.delete_details(tenantId)
        resp_json={
            'data':msg
        }
        return HttpResponse(json.dumps(resp_json),
                            content_type="application/json",
                            status=status.HTTP_200_OK)
    
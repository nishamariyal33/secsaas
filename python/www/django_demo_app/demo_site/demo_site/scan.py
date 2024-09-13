from django.http import Http404
from django.http import HttpResponse
from django.utils.decorators import method_decorator

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import json
import logging

from backend.redis import task
from demo_site import url_utils, settings
from backend.auth import ldap, token, hostedscan
from backend.email import smtp

job_id='celery-task-meta-'

logging.basicConfig(filename='/var/log/secsaas/token.log',
                    filemode='a',
                    format="%(asctime)s %(levelname)s pid:%(process)d "\
                           "%(funcName)s (%(filename)s:%(lineno)d) "\
                           "%(message)s",
                    level=logging.DEBUG)

class ScanServiceApi(APIView):
    parser_classes = [JSONParser]
    @method_decorator(url_utils.login_required, name='dispatch')
    def post(self, request):
        request_json = request.data
        # if(scan_type=="hostedscan"):
        #     hostedscanObj=hostedscan.Hostedscan()
        #     response=hostedscanObj.create_scan(target_url)
        #     logging.info("from scan service API")
        #     logging.info(response)
        #     resp_json = {
        #     'id': response,
        #     }
        #     return HttpResponse(json.dumps(resp_json),
        #                     content_type="application/json",
        #                     status=status.HTTP_200_OK)
        
        # return HttpResponse("Invalid Scan type",
        #                     status=status.HTTP_400_BAD_REQUEST)
        taskObj=task.create_job.delay(request_json, request.username)
        
        out={
            'id':taskObj.id,
            'state':taskObj.state,
            'status':taskObj.status,
            'requested_targets':[{'target':request_json.get('targetUrl')}],
            'type':request_json.get('type')
        }
        
        return HttpResponse(json.dumps(out),
                            content_type="application/json",
                            status=status.HTTP_200_OK)

class removeJobApi(APIView):
    parser_classes = [JSONParser]
    @method_decorator(url_utils.login_required, name='dispatch')
    def delete(self, request, job_id):
        response=task.remove_job(job_id)
        resp_json = {
                'message': "Job removed successfully",
                'jobId':job_id
       }
        return HttpResponse(json.dumps(resp_json),
                            content_type="application/json",
                            status=status.HTTP_200_OK)


class ScanResultApi(APIView):
    parser_classes = [JSONParser]
    @method_decorator(url_utils.login_required, name='dispatch')
    def get(self, request):
        request_json = request.data
        file_format=request_json.get('file_format')
        job_id=request_json.get('job_id', None)
        scan_type=request_json.get('scanType')
        if(scan_type=="hostedscan"):
            responseRedis=task.get_job_by_id(job_id)
            hostedscanObj=hostedscan.Hostedscan()
            response=hostedscanObj.get_scan_result(responseRedis.get('scanId'), file_format)
            return HttpResponse(response,
                            content_type="application/pdf",
                            headers={'Content-Disposition': 'attachment; filename="report.pdf"'},
                            status=status.HTTP_200_OK)
    
class ScanListApi(APIView):
    parser_classes = [JSONParser]
    @method_decorator(url_utils.login_required, name='dispatch')
    def get(self, request):
        request_json = request.data
        scan_type=request_json.get('scanType')
        if(scan_type=="hostedscan"):
            hostedscanObj=hostedscan.Hostedscan()
            #  hostedScanList=hostedscanObj.get_scan_list()
            redisScanList=task.get_jobs(request.username)
            # responseList=task.updated_scan_jobs(hostedScanList,redisScanList, request.username)
            responseJson={
                'data':redisScanList
            }
            return HttpResponse(json.dumps(responseJson),
                            content_type="application/json",
                            status=status.HTTP_200_OK)
            
class ScanDetailsApi(APIView):
    parser_classes = [JSONParser]
    @method_decorator(url_utils.login_required, name='dispatch')
    def get(self, request,job_id):
        request_json = request.data
        scan_type=request_json.get('scanType')
        if(scan_type=="hostedscan"):
            responseRedis=task.get_job_by_id(job_id)
            hostedscanObj=hostedscan.Hostedscan()
            responseScan=hostedscanObj.get_scan_by_id(responseRedis.get('scanId'))
            responseScan['jobId']=job_id
            responseScan['username']=request.username
            return HttpResponse(json.dumps(responseScan),
                            content_type="application/json",
                            status=status.HTTP_200_OK)

class ScanEmailApi(APIView):
    parser_classes = [JSONParser]
    @method_decorator(url_utils.login_required, name='dispatch')
    def post(self, request):
        try:
            request_json = request.data
            scan_type=request_json.get('scanType')
            job_id=request_json.get('job_id')
            file_format=request_json.get('file_format')
            if(scan_type=="hostedscan"):
                responseRedis=task.get_job_by_id(job_id)
                hostedscanObj=hostedscan.Hostedscan()
                response=hostedscanObj.send_scan_result(responseRedis.get('scanId'), file_format, request.username)
                return HttpResponse("Email Sent Successfully",
                                content_type="application/json",
                                status=status.HTTP_200_OK)
        except Exception as exc:
            logging.error("Cannot retrieve targets from except")
            logging.error(exc)
            return HttpResponse("Error in sending email",
                            status=status.HTTP_400_BAD_REQUEST)
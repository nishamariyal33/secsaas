from celery import Celery
from celery import shared_task
from django.http import Http404
from django.http import HttpResponse
from backend.auth import hostedscan
from rest_framework import status

import redis
import json
import time
import logging
from demo_site import celery_app
app = celery_app
r = redis.StrictRedis(host="172.26.0.3", port=6379, db=0)

logging.basicConfig(filename='/var/log/secsaas/token.log',
                    filemode='a',
                    format="%(asctime)s %(levelname)s pid:%(process)d "
                           "%(funcName)s (%(filename)s:%(lineno)d) "
                           "%(message)s",
                    level=logging.DEBUG)


@shared_task()
def create_job(request_json, username):
    """Sends an email when the feedback form has been submitted."""
    logging.info("Welcome to create_job")
    scan_type = request_json.get('scanType')
    target_url = request_json.get('targetUrl', None)
    scanName=request_json.get('type')
    time.sleep(5)
    if (scan_type == "hostedscan"):
        hostedscanObj = hostedscan.Hostedscan()
        try:
            response = hostedscanObj.create_scan(target_url, username, scanName)
        except Exception as exc:
            logging.error("Cannot create Job")
            logging.error(exc)
            raise

        scan_id = response['data']['id']

        while (response['data']['state'] != "SUCCEEDED"):
            response = hostedscanObj.get_scan_by_id(scan_id)
            time.sleep(20)
        response['username'] = username
        hostedscanObj.send_scan_result(scan_id, "pdf", username)
        return response


def get_jobs(username):
    """Sends an email when the feedback form has been submitted."""
    logging.info("Welcome to get_jobs")
    i = app.control.inspect()
    out_list = []
    active_tasks = i.active()

    if active_tasks:
        for worker_id in active_tasks:
            task_list = active_tasks[worker_id]
            for task in task_list:
                task_username = task['args'][1]
                if username != task_username:
                    continue
                requested_targets = []
                requested_targets.append({'target':task['args'][0]['targetUrl']})
                task_json = {
                    'jobId': task['id'],
                    'state': 'ACTIVE',
                    'status': 'ACTIVE',
                    'requested_targets': requested_targets,
                    'scanType': task['args'][0]['scanType'],
                    'username': task_username,
                    'type':task['args'][0]['type']

                }
                out_list.append(task_json)

    scheduled_tasks = i.scheduled()
    if (scheduled_tasks):
        for worker_id in scheduled_tasks:
            task_list = scheduled_tasks[worker_id]
            for task in task_list:
                task_username = task['args'][1]
                if username != task_username:
                    continue
                requested_targets = []
                requested_targets.append({'target':task['args'][0]['targetUrl']})
                task_json = {
                    'id': task['id'],
                    'state': 'SCHEDULED',
                    'status': 'SCHEDULED',
                    'requested_targets': requested_targets,
                    'scanType': task['args'][0]['scanType'],
                    'username': task_username,
                    'type':task['args'][0]['type']
                }
                out_list.append(task_json)

    reserved_tasks = i.reserved()
    if (reserved_tasks):
        for worker_id in reserved_tasks:
            task_list = reserved_tasks[worker_id]
            for task in task_list:
                task_username = task['args'][1]
                if username != task_username:
                    continue
                requested_targets = []
                requested_targets.append({'target':task['args'][0]['targetUrl']})
                task_json = {
                    'jobId': task['id'],
                    'state': 'RESERVED',
                    'status': 'RESERVED',
                    'requested_targets': requested_targets,
                    'scanType': task['args'][0]['scanType'],
                    'username': task_username,
                    'type':task['args'][0]['type']
                }
                out_list.append(task_json)

    cursor, keys = r.scan(match='celery-task-meta-*')
    dataObj = {}
    data = r.mget(keys)
    i = 0

    for key in data:
        my_json = key.decode('utf8').replace("'", '"')
        dataObj = json.loads(my_json)
        my_json_key = keys[i].decode('utf8').replace("'", '"')
        result = dataObj.get('result')
        dataVal = result.get('data')

        if result.get('username') != username:
            continue
        resultObj = {
            'status': dataVal.get("status"),
            # 'data':dataVal,
            'jobId': my_json_key,
            'username': username
        }

        for key1 in dataVal:
            resultObj[key1] = dataVal[key1]
        out_list.append(resultObj)
        i = i+1
    return out_list


def get_job_by_id(job_id):
    """Sends an email when the feedback form has been submitted."""
    logging.info("Welcome to get_job_by_id")
    dataObj = {}
    dataVal={}
    data = r.get(job_id)
    i = 0
    my_json = data.decode('utf8').replace("'", '"')
    dataObj = json.loads(my_json)
    resultObj = dataObj.get('result')
    if resultObj['data']:
           dataVal=resultObj.get('data')
    elif resultObj['id']:
           dataVal=resultObj['id']['data']
    resultObj = {
        'scanId': dataVal.get('id'),
        'jobId': job_id
    }
    return resultObj
#     scan_type = request_json.get('scanType')
#     target_url = request_json.get('targetUrl', None)

#     if (scan_type == "hostedscan"):
#        hostedscanObj = hostedscan.Hostedscan()
#        response = hostedscanObj.create_scan(target_url)
#        logging.info("from scan service API")
#        logging.info(response)
#        resp_json = {
#                 'id': response,
#        }
#        return resp_json


def remove_job(job_id):
    logging.info("Welcome to get_job_by_id")
    response = r.delete(job_id)
    return response


def updated_scan_jobs(hostedScanList, redisScanList, username):
    convertedList = convertList(hostedScanList)
    resultArr = []
    d1_map = {}
    d2_map = {}
    for d1_obj in convertedList:
        d1_id = d1_obj['id']
        d1_map[d1_id] = d1_obj
    for d2_raw in redisScanList:
        if d2_raw.get('username') != username:
            continue

        d2_obj = d2_raw.get('data')
        d2_id = d2_obj['id']
        d2_obj['username'] = d2_raw.get('username')
        d2_obj['job_id'] = d2_raw.get('jobId')
        d2_map[d2_id] = d2_obj

    for d1_id in d1_map:
        if d1_id in d2_map:
            d2_obj = d2_map[d1_id]
            d2_obj['state'] = d1_map[d1_id]['state']
            resultArr.append(d2_obj)

    return resultArr


def convertList(hostedScanList):
    my_json = hostedScanList.decode('utf8')
    json_object = json.loads(my_json)
    return json_object.get('data')

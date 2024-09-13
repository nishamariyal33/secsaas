from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import tempfile
from django.http import Http404
from django.http import HttpResponse
from django.utils.decorators import method_decorator

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pathlib import Path
from email.mime.text import MIMEText

from email.message import EmailMessage
import json
import logging

from demo_site import url_utils, settings
from backend.auth import ldap, token, hostedscan
from backend.tenant import tenant_api
logging.basicConfig(filename='/var/log/secsaas/token.log',
                    filemode='a',
                    format="%(asctime)s %(levelname)s pid:%(process)d "
                           "%(funcName)s (%(filename)s:%(lineno)d) "
                           "%(message)s",
                    level=logging.DEBUG)

gmail_user = 'secsaasvt@gmail.com'
gmail_password = 'ojbndgxwfktllrqe'


def sendReport(scan_details, file_response, username):
    try:
        subject = 'Vulnerability Scan Result'

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user,gmail_password)
        # Craft message (obj)
        msg = MIMEMultipart()

        message = f'{"Hi, Here is the vulnerability scan result requested by you. Please find the attached PDF"}\n'
        msg['Subject'] = subject
        msg['From'] = gmail_user
        msg['To'] = "kishoreh@vt.edu, nishamariyalr@vt.edu"
        # Insert the text to the msg going by e-mail
        msg.attach(MIMEText(message, "plain"))
        # Attach the pdf to the msg going by e-mail
        attach = MIMEApplication(file_response,_subtype="pdf")
        attach.add_header('Content-Disposition','attachment',filename=str("result.pdf"))
        msg.attach(attach)
        # send msg
        server.send_message(msg)
        return
        
    except Exception as exc:
        logging.error("Error in sending email sendReport()")
        logging.error(exc)
        raise
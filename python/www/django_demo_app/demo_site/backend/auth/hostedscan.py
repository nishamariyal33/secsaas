#!/usr/bin/python
import time
import json
import requests
import logging
from backend.email import smtp

logging.basicConfig(filename='/var/log/secsaas/token.log',
                    filemode='a',
                    format="%(asctime)s %(levelname)s pid:%(process)d "\
                           "%(funcName)s (%(filename)s:%(lineno)d) "\
                           "%(message)s",
                    level=logging.DEBUG)

# #username and password for loging in 
HOSTEDSCAN_URL="https://api.hostedscan.com"
HOSTEDSCAN_HEADERS = {'X-HOSTEDSCAN-API-KEY': 'key_dc5cb88d97a76837507ef051c2787fbd665b8044599e0f31', 'content-type': 'application/json'}     # header containing token, it also specifies
# username = "admin"
# password = "admin"


# #Alter the url filled if Hostedscan is running on a remote machine
# url = "https://localhost:8834"

# #Make it true if you want to verify the SSL certificate
# verify = False


# #Disables Warning when not verifying SSL certs
# requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# #Checks if the target is specified or configure flag is set, when -p flag is used
# if args.policy_name:
#     if not (args.target or args.target_file or args.configure):
#         print "usage: " + usage
#         print"python-nessus -h for more info"
#         exit()

# #Checks if the policy to use is defined or not, when -t or -T flag is used
# if args.target or args.target_file:
#     if not args.policy_name:
#         print "usage: " + usage
#         print"python-nessus -h for more info"
#         exit()


# #Tries to open target file if -T flag is used
# if args.target_file:
#     try:
#         with open(args.target_file) as t:
#             target=t.read()
#     except IOError:
#         print"Cannot open the file",args.target_file
#         print"Make sure you spelled it right\n"
#         exit()

# #set target variable when -t flag is used
# if args.target:
#     target=args.target


# #if --configure flag is set, configure the policy before launching the scan
# if args.configure:
    # if not args.policy_name:
    #     print"Policy name not supplied"
    #     print"python-nessus -h for more info"
    #     exit()

class Hostedscan(object):
   
    def get_target_id(self,target_url):
        """ Function to retrieve policies:
            This Function retrieves policies in two phases:
            First it retrieves the user defined policies and then the predefined templates"""
        logging.info(HOSTEDSCAN_URL)
        try:
            response = requests.get(HOSTEDSCAN_URL+"/v1/targets",headers=HOSTEDSCAN_HEADERS)         #Getting templates
            if response.status_code!=200:
                logging.error("Cannot retrieve targets")
                logging.error(response.json())
                return
                # return targets.json()['targets'],targets.json()['templates']        #return json data as tuple
            targets=response.json()
            for target in targets['data']:
                if target['target']==target_url:
                    return target['id']
            raise ValueError("Target not added")
        except Exception as exc:
            logging.error("Cannot retrieve targets from except")
            logging.error(exc)
            raise
    
    def add_target(self,target_url):
        logging.info(target_url)
        try:
            payload = {
                "target":target_url, 
                "tags":[]
            }
            response = requests.post(
                HOSTEDSCAN_URL+"/v1/targets",
                json=payload,
                headers=HOSTEDSCAN_HEADERS)         #Getting templates
            if response.status_code==200 or (response.status_code==400 and 'Target already exists' in response.json()['error']):
                return
            else:
                logging.error("Cannot post targets")
                logging.error(response.json())
                raise Exception("Cannot create target")
        except Exception as exc:
            logging.error("Cannot retrieve targets from except")
            logging.error(exc)
            raise
    
    def create_scan(self, target_url, username, scanName):
        try:
            logging.info("11111111111111111")
            logging.info(scanName)
            Hostedscan.add_target(self,target_url)
            target_id=Hostedscan.get_target_id(self,target_url)
            payload = {"target_ids": [target_id], "type": scanName}
            response = requests.post(
                HOSTEDSCAN_URL+"/v1/scans",
                json=payload,
                headers=HOSTEDSCAN_HEADERS)         #Getting templates

            if response.status_code==200:
                responseJson=response.json()
                responseJson['username']=username
                return responseJson
            else:
                logging.error("Cannot create scans")
                logging.error(response.error)
                raise Exception("Cannot create scans")
        except Exception as exc:
            logging.error("Cannot create scan from except")
            logging.error(exc)
            raise
            
    def get_result_by_id(self, scan_id, file_format):
        logging.info("Welcome to get_result_by_id")
        try:
            response = requests.get(HOSTEDSCAN_URL+"/v1/scans/"+scan_id,headers=HOSTEDSCAN_HEADERS)         #Getting templates
            if response.status_code!=200:
                logging.error("Cannot retrieve scan for given scan_id")
                logging.error(response.json())
                return
                # return targets.json()['targets'],targets.json()['templates']        #return json data as tuple
            targets=response.json()
            for target in targets['data']['results']:
                if file_format in target['content_type']:
                    return target['result_id']
            raise ValueError("Target not added")
        except Exception as exc:
            logging.error("Cannot retrieve scans from except")
            logging.error(exc)
            raise
        
    def get_scan_by_id(self, scan_id):
        logging.info("Welcome to get_scan_by_id")
        try:
            response = requests.get(HOSTEDSCAN_URL+"/v1/scans/"+scan_id,headers=HOSTEDSCAN_HEADERS)         #Getting templates
            if response.status_code!=200:
                logging.error("Cannot retrieve scan for given scan_id")
                logging.error(response.json())
                return
                # return targets.json()['targets'],targets.json()['templates']        #return json data as tuple
            targets=response.json()
            logging.info(targets)
            return targets
        except Exception as exc:
            logging.error("Cannot retrieve scans from except")
            logging.error(exc)
            raise
            
            
    def get_scan_result(self, scan_id, file_format):
        logging.info("Welcome to get_scan_result")
        try:
            result_id = Hostedscan.get_result_by_id(self,scan_id,file_format)
            logging.info(result_id)
            response = requests.get(HOSTEDSCAN_URL+"/v1/results/"+result_id,headers=HOSTEDSCAN_HEADERS)
            return response.content
        except Exception as exc:
          
            logging.error("Cannot retrieve targets from except from get_scan_result")
            logging.error(exc)
            raise
    
    def send_scan_result(self, scan_id, file_format, username):
        logging.info("Welcome to send_scan_result")
        try:
            response=Hostedscan.get_scan_result(self,scan_id,file_format)
            scan_details=Hostedscan.get_scan_by_id(self,scan_id)
            res=smtp.sendReport(scan_details,response,username)
            # return response.content
            return
        except Exception as exc:
          
            logging.error("Cannot retrieve targets from except")
            logging.error(exc)
            raise

    def get_scan_list(self):
        try:
            response = requests.get(HOSTEDSCAN_URL+"/v1/scans/",headers=HOSTEDSCAN_HEADERS)
            return response.content
        except Exception as exc:
          
            logging.error("Cannot retrieve scans from except")
            logging.error(exc)
            raise
    # def policy_json_from_policy_name():
    #     """This function is used to get the json data from the policy name.
    #     The function checks for the existence of policy name supplied with -p tag
    #     and returns the complete json data of the file."""
        
    #     policies = Hostedscan.get_policies()                                 #Getting policies as a tuple
    #     for policy in policies[0]:                   #checks if the policy to use is predefined-template,if so,return the policy json
    #         if args.policy_name==policy['name']:
    #             return policy
    #     for policy in policies[1]:                         #checks if the policy to use is user-defined, if so,return the policy json
    #         if args.policy_name==policy['title']:         
    #             return policy
    #     print"Cannot find the policy with name",args.policy_name
    #     logout()      


    def delete_scan(self,scan_id):
        res = requests.delete(Hostedscan.url + '/scans/{0}'.format(scan_id),headers=Hostedscan.headers,verify=Hostedscan.verify)
        if res.status_code==200:
            logging.info("Scan deleted")
        else:
            logging.error (res.json()['error'])
        Hostedscan.logout()


    # def configure_policy():
    #     """Function to configure policy settings.
    #     This function can be useful when trying to configure the policy prior to launching the scan"""

    #     policy = policy_json_from_policy_name()                    #getting policy json data from its name

    #     try:
    #         policy_id=policy['id']
    #     except KeyError:
    #         print"Only User-defined policies can be configured"
    #         logout()

    #     #Getting policy configurations
    #     res = requests.get(url+'/policies/{0}'.format(policy['id']),verify=False,headers=headers)

    #     #If response is not ok, print the error and logout
    #     if res.status_code!=200:
    #         print res.json()['error']
    #         logout()

    #     #If response is ok, ensure that the discovery mode is set to custom
    #     if res.json()['settings']['discovery_mode']!='Custom':
    #         payload = res.json()
    #         payload['settings']['discovery_mode']="Custom"
    #         payload=json.dumps(payload)
    #         res = requests.put(url+'/policies/{0}'.format(policy['id']),verify=False,headers=headers,data=payload)

    #         if res.status_code!=200:
    #             print res.json()['error']
    #             logout()

    #     payload = requests.get(url+'/policies/{0}'.format(policy['id']),verify=False,headers=headers).json()
    #     print"Trying to configure the policy"
    #     try:
    #         #Configure user-defined policy at run time

    #         print colored("\nAnytime press Enter for default :\n",'green',attrs=['bold'])
    #         print "Ping the remote host" + "(default is " + payload['settings']['ping_the_remote_host']  + ") : ",
    #         temp = raw_input()

    #         #when ping the remote host option is changed, we need to get the policy json data again to handle key error

    #         #if ping_the_remote_host option is changed, getting the payload again
    #         if not (temp=="" or payload['settings']['ping_the_remote_host']==temp):
    #             payload['settings']['ping_the_remote_host']=temp
    #             payload=json.dumps(payload)
    #             res = requests.put(url+'/policies/{0}'.format(policy['id']),verify=False,headers=headers,data=payload)
    #             payload = requests.get(url+'/policies/{0}'.format(policy['id']),verify=False,headers=headers).json()


    #         if payload['settings']['ping_the_remote_host']=='yes':               #if pinging the remote host is enabled, ask for various pinging option
    #             print colored("\nPING METHODS : ",'blue',attrs=['bold'])
    #             print "ICMP ping" + "(default " + payload['settings']['icmp_ping']  + ") : ",
    #             temp = raw_input()
    #             if temp!="":
    #                 payload['settings']['icmp_ping']=temp
    #             print "TCP ping" + "(default " + payload['settings']['tcp_ping'] + ") : ",
    #             temp = raw_input()
    #             if temp!="":
    #                 payload['settings']['tcp_ping']=temp
    #             print "UDP ping" + "(default " + payload['settings']['udp_ping']  + ") : ",
    #             temp = raw_input()
    #             if temp!="":
    #                 payload['settings']['udp_ping']=temp
    #             print "ARP ping" + "(default " + payload['settings']['arp_ping'] + ") : ",
    #             temp = raw_input()
    #             if temp!="":
    #                 payload['settings']['arp_ping']=temp

    #         #Taking portscan range from user
    #         print colored("\nPORT SCAN RANGE",'blue',attrs=['bold'])
    #         print "Port Scan range " + "(default is " + payload['settings']['portscan_range'] + ") : ",
    #         temp = raw_input()
    #         if temp!="":
    #             payload['settings']['portscan_range']=temp

    #         #Determining which network port scanners to use
    #         print colored("\nNETWORK PORT SCANNERS",'blue',attrs=['bold'])
    #         print "TCP " + "(default " + payload['settings']['tcp_scanner']  + ") : ",
    #         temp = raw_input()
    #         if temp!="":
    #             payload['settings']['tcp_scanner']=temp
    #         print "SYN " + "(default " + payload['settings']['syn_scanner'] + ") : ",
    #         temp = raw_input()
    #         if temp!="":
    #             payload['settings']['syn_scanner']=temp
    #         print "UDP " + "(default " + payload['settings']['udp_scanner'] + ") : ",
    #         temp = raw_input()
    #         if temp!="":
    #             payload['settings']['udp_scanner']=temp

    #         #sending put request to /policies to update the changes requested
    #         print"Updating the policy "
    #         payload=json.dumps(payload)
    #         res = requests.put(url+'/policies/{0}'.format(policy['id']),verify=False,headers=headers,data=payload)

    #         if res.status_code==200:
    #             print"Policy updated Successfully"
    #         else:
    #             print res.json()['error']

    #     except KeyError:
    #         print "key error code executed",
    #         raw_input()
    #         exit()


    def show_status(scan_id):
        while True:
            status = requests.get(Hostedscan.url + '/scans/' + str(scan_id),headers=Hostedscan.headers,verify=Hostedscan.verify)
            status = status.json()['info']['status']
            if status=='canceled':
                logging.info("Scan has been canceled")
                logging.info("Logging the user out")
                Hostedscan.logout()
            if status=='paused':
                logging.info("Scan has been paused")
                logging.info("Logging the user out")
                Hostedscan.logout()
            if status=='completed':
                break
            if status=='running':
                time.sleep(2)

    def export_request(scan_id,export_format,password):
        """Function to request for the export of scan result.
        It takes scan ID of the scan and tries to export the report in the specified format"""

        logging.info("Trying to export the report")
        if export_format == 'csv' or export_format == 'nessus': 
            payload =  { "format" : export_format }
        elif export_format =='db': 
            payload =  { "format" : export_format , "password":password}
        elif export_format=='pdf' or export_format=='html':
            payload = { "format":export_format, "chapters":"vuln_hosts_summary"}
        else:
            logging.error("Unsupported format selected\nPlease select a valid format")
            Hostedscan.logout()
        payload = json.dumps(payload)
        res = requests.post(Hostedscan.url + '/scans/' + str(scan_id) + '/export',data=payload,verify=Hostedscan.verify,headers=Hostedscan.headers)
        if res.status_code==200:
            file_id = res.json()['file']
            logging.info("Waiting for the report to be ready to download...")
            time.sleep(2)
            while Hostedscan.export_status(scan_id,file_id) is False:
                time.sleep(1)
            Hostedscan.export_download(scan_id,file_id)
        else:
            logging.error (res.json()['error'])
            logging.error("Waiting for 10 seconds before retrying...")
            time.sleep(10)
            Hostedscan.export_request(scan_id)



    def export_status(scan_id,file_id):
        """This function checks the status of the export file.
        It returns false until the report is ready for downloading"""

        res = requests.get(Hostedscan.url + '/scans/{0}/export/{1}/status'.format(scan_id,file_id),headers=Hostedscan.headers,verify=Hostedscan.verify)
        return res.json()['status']=='ready'



    def export_download(scan_id,file_id,export_format):
        """Function to download the report when it is ready"""

        logging.info("Report is ready to download")
        logging.info("Trying to download the report")
        res = requests.get(Hostedscan.url + '/scans/' + str(scan_id) + '/export/' + str(file_id) +'/download',headers=Hostedscan.headers,verify=Hostedscan.verify)
        if res.status_code!=200:
            logging.error (res.json()['error'] + '\nTrying again')
            Hostedscan.export_download(scan_id,file_id)
        else:
            logging.info("Report downloaded")
            logging.info("Storing the report downloaded")
            filename = 'nessus_{0}_{1}.{2}'.format(scan_id,file_id,export_format)
            with open(filename,'wb') as f:
                f.write(res.content)

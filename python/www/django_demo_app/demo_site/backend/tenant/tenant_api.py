import random
import string
from backend.sql_utils import mysql
import logging


logging.basicConfig(filename='/var/log/secsaas/token.log',
                    filemode='a',
                    format="%(asctime)s %(levelname)s pid:%(process)d "\
                           "%(funcName)s (%(filename)s:%(lineno)d) "\
                           "%(message)s",
                    level=logging.DEBUG)

COL_ID=0
COL_NAME=1
COL_ADDR=2
COL_EMAIL=3
COL_ADURL=4
COL_BASEDN=5
def __generate_random_id(size=15, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_tenant(name, address, adUrl,email,baseDn):
    tenantId = __generate_random_id()
    val = (tenantId, name, address, adUrl,email, baseDn)
    logging.info("qqqq ",val)
    sql = "INSERT INTO tenant (tenantId, name, address, adUrl, email, baseDn) VALUES (%s, %s, %s, %s, %s, %s)"
    mysql.execute_insert_sql(sql,val)
    return tenantId

def get_tenant_ad(tenantId):
    args=(tenantId,)
    sql = "SELECT * from tenant where tenantId=%s"
    row=mysql.execute_select_sql(sql,args)
    logging.info("hhhhh %s",row)
    if not row:
        raise ValueError('Invalid Tenant')

    return row[COL_ADURL],row[COL_BASEDN]

def get_tenant_details(tenantId):
    args=(tenantId,)
    sql = "SELECT * from tenant where tenantId=%s"
    row=mysql.execute_select_sql(sql,args)
    logging.info(row)
    if not row:
        raise ValueError('Invalid Tenant')

    return row

def delete_details(tenantId):
    args=(tenantId,)
    sql = "DELETE from tenant where tenantId=%s"
    var=mysql.execute_insert_sql(sql,args)
    logging.info(var)
    logging.info("DELETED")
   
    return "DELETED SUCCESSFULLY"
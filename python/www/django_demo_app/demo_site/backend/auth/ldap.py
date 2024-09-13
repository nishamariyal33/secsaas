import os
import ldap
import logging
from backend.tenant import tenant_api
logging.basicConfig(filename='/var/log/secsaas/ldap.log',
                    filemode='a',
                    format="%(asctime)s %(levelname)s pid:%(process)d "\
                           "%(funcName)s (%(filename)s:%(lineno)d) "\
                           "%(message)s",
                    level=logging.DEBUG)


class LdapConn(object):
    """
    Helper class for doing ldap stuff. Includes APIs to authenticate user, get
    details about user, etc
    """
    def __init__(self,adUrl,baseDn):
        logging.info("Initializing LDAP con with %s and %s", adUrl,baseDn)
        if not adUrl.startswith("ldap://"):
            adUrl = "ldap://" + adUrl +":389"
        
        
        self.ldap_conn = ldap.initialize(adUrl)
        self.user_base_dn = baseDn
        self.bind_done = False

    def bind(self, username, password):
        try:
            self.ldap_conn.simple_bind_s(username, password)
        except ldap.INVALID_CREDENTIALS:
            logging.warning("Invalid credentials for %s", username)
            return False
        except ldap.LDAPError as e:
            if type(e) == dict and e.has_key('desc'):
                err_msg = e['desc']
            else:
                err_msg = e

            logging.error("Ldap Connection failure. Reason: %s", e)
            return False
        except Exception as e:
            logging.error("Cannot bind user. Reason: %s", e)
            return False

        self.bind_done = True
        return True

    def get_user_info(self, username):
        return {}


def ldap_user_login(tenantId, username, password):
    adUrl,baseDn=tenant_api.get_tenant_ad(tenantId)
    ldap_conn_obj = LdapConn(adUrl,baseDn)
    if not ldap_conn_obj.bind(username, password):
        return False, None

    return True, ldap_conn_obj.get_user_info(username)


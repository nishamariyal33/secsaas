import time
import jwt
import logging

logging.basicConfig(filename='/var/log/secsaas/token.log',
                    filemode='a',
                    format="%(asctime)s %(levelname)s pid:%(process)d "\
                           "%(funcName)s (%(filename)s:%(lineno)d) "\
                           "%(message)s",
                    level=logging.DEBUG)


SECSAAS_PREFIX = "SECSAAS:"

def create_auth_token(secret, username,tenantId,
                      expiration=3600, #60 minutes
                      algo="HS256"):
    curr_time = time.time()
    exp_time = curr_time + expiration

    data = {
        'username': username,
        'tenantId':tenantId,
        'start_time': curr_time,
        'exp_time': exp_time
    }

    return SECSAAS_PREFIX + jwt.encode(data, secret, algorithm=algo)

def validate_token(secret, encoded_token, algo="HS256"):
    token_list = encoded_token.split(SECSAAS_PREFIX)
    if len(token_list) != 2:
        logging.warning("Invalid token passed: %s", encoded_token)
        return False, None

    actual_token = token_list[1]

    try:
        data = jwt.decode(actual_token, secret, algorithms=[algo])
    except Exception as exc:
        logging.warning("Invalid token passed: %s", encoded_token)
        return False, None

    curr_time = time.time()
    if curr_time > data['exp_time']:
        logging.warning("Expired token: %s", encoded_token)
        return False, None

    return True, data['username']

def decode_token(secret, encoded_token, algo="HS256"):
    token_list = encoded_token.split(SECSAAS_PREFIX)
    if len(token_list) != 2:
        logging.warning("Invalid token passed: %s", encoded_token)
        return False, None

    actual_token = token_list[1]

    try:
        data = jwt.decode(actual_token, secret, algorithms=[algo])
        logging.info(data)
        resp={
            'username':data['username'],
            'tenantId':data['tenantId']
        }
        return resp
    except Exception as exc:
        logging.warning("Invalid token passed: %s", encoded_token)
        return False, None
   


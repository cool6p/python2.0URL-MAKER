# -*- coding: utf8 -*-
import base64
import hashlib
import hmac
import time
import random

import requests
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

secret_id = ""
secret_key = ""

def get_string_to_sign(method, endpoint, params):
    s = method + endpoint + "/v2/index.php?"
    query_str = "&".join("%s=%s" % (k, data[k]) for k in sorted(data))
    return s + query_str

def sign_str(key, s, method):
    hmac_str = hmac.new(key.encode("utf8"), s.encode("utf8"), method).digest()
    return base64.b64encode(hmac_str)

if __name__ == '__main__':
    # 请求域名\ACTION注意修改 
    endpoint = "cns.api.qcloud.com"
    data = {
        'Action' : 'RecordCreate',
        'Nonce' : 382823,
        'SecretId' : secret_id,
        'Timestamp' :int(time.time()),
        'region':'gz',
        'domain':'wainsun.com',
        'subDomain':'www',
        'recordType':'A',
        'recordLine':'默认',
        'value':'192.29.29.29'
    # 参数后面按文档添加   
    }
    s = get_string_to_sign("GET", endpoint, data)
    data["Signature"] = sign_str(secret_key, s, hashlib.sha1)
    print(data["Signature"])
    # 此处会实际调用，成功后可能产生计费
    resp = requests.get("https://" + endpoint + "/v2/index.php", params=data)
    print(resp.url)
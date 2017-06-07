# -*- coding: utf-8 -*-
# version: 3.5

import sys
import urllib.request
import json


if __name__ == '__main__':

    # [CODE 1]
    page_name = "jtbcnews"
    app_id = "200920440387013"
    app_secret = "daccef14d5cd41c0e95060d65e66c41d"
    access_token = app_id + "|" + app_secret

    # [CODE 2]
    # https://graph.facebook.com/v2.8/[page_id]/?access_token=[App_ID]|[Secret_Key]
    # 형식의 문자열을 만들어 낸다

    base = "https://graph.facebook.com/v2.8"
    node = "/" + page_name
    parameters = "/?access_token=%s" % access_token
    url = base + node + parameters
    
    # [CODE 3]
    req = urllib.request.Request(url)
    
    # [CODE 4]
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            data = json.loads(response.read().decode('utf-8'))
            page_id = data['id']
            print ("%s Facebook Numeric ID : %s" % (page_name, page_id))
    except Exception as e:
        print (e)

        
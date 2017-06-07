# -*- coding: utf-8 -*-
# version: 3.5

import sys
import urllib.request
import json

if __name__ == '__main__':

    # [CODE 1]
    page_name = "jtbcnews"
    page_id = "240263402699918"
    app_id = "200920440387013"
    app_secret = "daccef14d5cd41c0e95060d65e66c41d"
    
    # [CODE 2]
    from_date = "2017-01-01"
    to_date = "2017-01-31"
    num_statuses = "10"
    access_token = app_id + "|" + app_secret

    # [CODE 3] 
    base = "https://graph.facebook.com/v2.8"
    node = "/%s/posts" % page_id 
    fields = "/?fields=id,message,link,name,type,shares,reactions," + \
             "created_time,comments.limit(0).summary(true)" + \
             ".limit(0).summary(true)"
    duration = "&since=%s&until=%s" % (from_date, to_date)
    parameters = "&limit=%s&access_token=%s" % (num_statuses, access_token)
    url = base + node + fields + duration + parameters

    req = urllib.request.Request(url)
    
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            data = json.loads(response.read().decode('utf-8'))
            print (data)
            
    except Exception as e:
        print (e)


'''
{
  "data": [
     ... Endpoint data is here
  ], 
  "paging": {
    "cursors": {
      "after": "MTAxNTExOTQ1MjAwNzI5NDE=",
      "before": "NDMyNzQyODI3OTQw"
    },
    "previous": "https://graph.facebook.com/me/albums?limit=25&before=NDMyNzQyODI3OTQw"
    "next": "https://graph.facebook.com/me/albums?limit=25&after=MTAxNTExOTQ1MjAwNzI5NDE="
  }
}

{
  "data": [
     ... Endpoint data is here
  ],
  "paging": {
    "previous": "https://graph.facebook.com/me/feed?limit=25&since=1364849754",
    "next": "https://graph.facebook.com/me/feed?limit=25&until=1364587774"
  }
}

{
    "data":[
        {
            "comments":{
                "data":[
                ],
                "summary":{
                    "order":"ranked",
                    "total_count":12,
                    "can_comment":"False"
                }
            },
            "message":"즉 청와대가 최 씨의 국정개입 사건을 파 악하고도 \n은폐했다는 사실이 안 전 수석 입에서 나온 겁니다.",
            "type":"link",
            "s hares":{
                "count":44
            },
            "reactions":{
                "data":[
                ],
                "summary":{
                    "viewer_reaction":"NONE",
                    "total_count":437
                }
            },
            "created_time":"2017-02-23T00:00:00+0000",
            "name":"안종범 \"재단 임원 인사에 최순실 개입, 알고도 숨겼다\"",
            "id":"240263402699918 _1328805163845731",
            "link":"http://news.jtbc.joins.com/article/article.aspx?new s_id=NB11427906&pDate=20170222"
        }
    ],
    "paging":{
        "next":"https://graph.facebook.co m/v2.8/240263402699918/posts?fields=...",
        "previous":"https://graph.facebook.com/v2.8/240263402699918/posts?fields=..."
    }
}
'''
# -*- coding: utf8 -*-
# version: 3.5

import sys
import urllib.request
import json
import datetime
import csv
import time

#[CODE 1]
def get_request_url(url):
    
    req = urllib.request.Request(url)
         
    try: 
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print ("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

#[CODE 2]
def getFacebookNumericID(page_id, access_token):
    
    base = "https://graph.facebook.com/v2.8"
    node = "/" + page_id
    parameters = "/?access_token=%s" % access_token
    url = base + node + parameters
    
    retData = get_request_url(url)
    
    if (retData == None):
        return None
    else:
        jsonData = json.loads(retData)
        return jsonData['id']

#[CODE 3]
def getFacebookPost(page_id, access_token, from_date, to_date, num_statuses):
    
    base = "https://graph.facebook.com/v2.8"
    node = "/%s/posts" % page_id 
    fields = "/?fields=id,message,link,name,type,shares,reactions," + \
             "created_time,comments.limit(0).summary(true)" + \
             ".limit(0).summary(true)"
    duration = "&since=%s&until=%s" % (from_date, to_date)
    parameters = "&limit=%s&access_token=%s" % (num_statuses, access_token)
    url = base + node + fields + duration + parameters

    retData = get_request_url(url)

    if (retData == None):
        return None
    else:
        return json.loads(retData)


def getPostItem(post, key):
    try:
        if key in post.keys():
            return post[key]
        else:
            return ''
    except:
        return ''

def getPostTotalCount(post, key):
    try:
        if key in post.keys():
            return post[key]['summary']['total_count']
        else:
            return 0
    except:
        return 0

#[CODE 4]
def getPostData(post, access_token, jsonResult):
    
    #[CODE 4-1]
    post_id = getPostItem(post, 'id')
    post_message = getPostItem(post, 'message')
    post_name = getPostItem(post, 'name')
    post_link = getPostItem(post, 'link')
    post_type = getPostItem(post, 'type')
   
    post_num_reactions = getPostTotalCount(post, 'reactions')
    post_num_comment = getPostTotalCount(post, 'comments')
    post_num_shares = 0 if 'shares' not in post.keys() else post['shares']['count']

    #[CODE 4-2]
    post_created_time = getPostItem(post, 'created_time')
    post_created_time = datetime.datetime.strptime(post_created_time, '%Y-%m-%dT%H:%M:%S+0000')
    post_created_time = post_created_time + datetime.timedelta(hours=+9)
    post_created_time = post_created_time.strftime('%Y-%m-%d %H:%M:%S')

    #[CODE 4-3] 
    reaction = getFacebookReaction(post_id, access_token) if post_created_time > '2016-02-24 00:00:00' else {}
    post_num_likes = getPostTotalCount(reaction, 'like')
    post_num_likes = post_num_reactions if post_created_time < '2016-02-24 00:00:00' else post_num_likes
    
    #[CODE 4-4]
    post_num_loves = getPostTotalCount(reaction, 'love')
    post_num_wows = getPostTotalCount(reaction, 'wow')
    post_num_hahas = getPostTotalCount(reaction, 'haha')
    post_num_sads = getPostTotalCount(reaction, 'sad')
    post_num_angrys = getPostTotalCount(reaction, 'angry')
    
    jsonResult.append({'post_id':post_id, 'message':post_message,
                    'name':post_name, 'link':post_link, 
                    'created_time':post_created_time, 'num_reactions':post_num_reactions,
                    'num_comments':post_num_comment, 'num_shares':post_num_shares,
                    'num_likes':post_num_likes, 'num_loves':post_num_loves,
                    'num_wows':post_num_wows, 'num_hahas':post_num_hahas,
                    'num_sads':post_num_sads, 'num_angrys':post_num_angrys})

    
#[CODE 5]
def getFacebookReaction(post_id, access_token):

    base = "https://graph.facebook.com/v2.8"
    node = "/%s" % post_id
    reactions = "/?fields=" \
                "reactions.type(LIKE).limit(0).summary(total_count).as(like)" \
                ",reactions.type(LOVE).limit(0).summary(total_count).as(love)" \
                ",reactions.type(WOW).limit(0).summary(total_count).as(wow)" \
                ",reactions.type(HAHA).limit(0).summary(total_count).as(haha)" \
                ",reactions.type(SAD).limit(0).summary(total_count).as(sad)" \
                ",reactions.type(ANGRY).limit(0).summary(total_count).as(angry)"
    parameters = "&access_token=%s" % access_token
    url = base + node + reactions + parameters

    retData = get_request_url(url)

    if (retData == None):
        return None
    else:
        return json.loads(retData)    

#[CODE 6]
def main():
    page_name = "chosun"
    app_id = "200920440387013"
    app_secret = "daccef14d5cd41c0e95060d65e66c41d"
    access_token = app_id + "|" + app_secret
   
    from_date = '2016-10-01'
    to_date = '2017-03-12'
    
    num_posts = 50
    go_next = True
    jsonResult = []

    page_id = getFacebookNumericID(page_name, access_token)

    if (page_id == None):
        print ("[%s] %s is Invalid Page Name" % (datetime.datetime.now(), page_name))
        exit()
    
    print ("[%s] %s page id is %s" % (datetime.datetime.now(), page_name, page_id))

    #[CODE 6-1]
    jsonPost = getFacebookPost(page_id, access_token, from_date, to_date, num_posts)

    if (jsonPost == None):
        print ("No DATA")
        exit()

    #[CODE 6-2]
    while (go_next):
        for post in jsonPost['data']:
            getPostData(post, access_token, jsonResult)
            
        if 'paging' in jsonPost.keys():
            jsonPost =  json.loads(get_request_url(jsonPost['paging']['next']))
        else:
            go_next = False
    
    #[CODE 6-3]
    with open('%s_facebook_%s_%s.json' % (page_name, from_date, to_date), 'w', encoding='utf8') as outfile:
        str_ = json.dumps(jsonResult,
                      indent=4, sort_keys=True,
                      ensure_ascii=False)
        outfile.write(str_)
        
    print ('%s_facebook_%s_%s.json SAVED' % (page_name, from_date, to_date))

if __name__ == '__main__':
    main()

    


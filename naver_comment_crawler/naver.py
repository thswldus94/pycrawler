import requests
import os
#from bs4 import BeautifulSoup
from urllib import parse
import json

# const
target_url = 'https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=102&oid=003&aid=0009837633'
# target url 의 sid, oid, aid 등 필요한 url 파라미터로 조정
base_comment_api_url = 'http://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&pool=cbox5&lang=ko&country=KR&pageSize=100&indexSize=100&listType=OBJECT&page=1'
# page 수를 1부터 늘려가면서 체크
# pageSize 와 indexSize는 기호대로 조정
# sort=Favorite 붙이면 인기순으로 볼수있음
# 뚱치기 화이팅 >.<

def parse_url_get_content(url_str, base_comment_api_url):
    url_dict = parse.urlparse(url_str)
    params = parse.parse_qs(url_dict.query)

    oid = params['oid'][0]
    aid = params['aid'][0]

    #&objectId=news003,0009837633
    comment_api_url = base_comment_api_url + "&objectId=news" + parse.quote(oid + "," + aid)
    print(comment_api_url)
    
    #define header
    header = {"referer" : url_str}
    # get comment
    res = requests.get(comment_api_url, headers = header)
    parse_content(res.content)
    #print(res.content)


def parse_content(content):
    decoded_content = content.decode()
    #fix_content = content.replace("_callback(", "")[:-1]
    json_content = decoded_content.replace("_callback(", "")[:-2]
    parsed_json = json.loads(json_content)

    comment_list = parsed_json['result']['commentList']
    #print(comment_list)

    for i in range(len(comment_list)):
        comment = comment_list[i]
        print("[" + comment['userName'] + "]" + " : " + comment['contents'] + " (" + comment['modTime'] + ')')
            


#request_content(target_url)
parse_url_get_content(target_url, base_comment_api_url)






# 샘플 데이터
# {
#     "ticket": "news",
#     "objectId": "news003,0009837633",
#     "categoryId": "*",
#     "templateId": "view_society",
#     "commentNo": 2135966025,
#     "parentCommentNo": 2135966025,
#     "replyLevel": 1,
#     "replyCount": 0,
#     "replyAllCount": 0,
#     "replyPreviewNo": null,
#     "replyList": null,
#     "imageCount": 0,
#     "imageList": null,
#     "imagePathList": null,
#     "imageWidthList": null,
#     "imageHeightList": null,
#     "commentType": "txt",
#     "stickerId": null,
#     "sticker": null,
#     "sortValue": 1588044245575,
#     "contents": "해외 유입만 제대로 막아도 코로아 0명 나오겟다.   2주간만 해외 유입을 막아봐요",
#     "userIdNo": "uOuY",
#     "exposedUserIp": null,
#     "lang": "ko",
#     "country": "KR",
#     "idType": "naver",
#     "idProvider": "naver",
#     "userName": "heez****",
#     "userProfileImage": "",
#     "profileType": "naver",
#     "modTime": "2020-04-28T12:24:05+0900",
#     "modTimeGmt": "2020-04-28T03:24:05+0000",
#     "regTime": "2020-04-28T12:24:05+0900",
#     "regTimeGmt": "2020-04-28T03:24:05+0000",
#     "sympathyCount": 21,
#     "antipathyCount": 6,
#     "userBlind": false,
#     "hideReplyButton": false,
#     "status": 0,
#     "mine": false,
#     "best": false,
#     "mentions": null,
#     "toUser": null,
#     "userStatus": 0,
#     "categoryImage": null,
#     "open": false,
#     "levelCode": null,
#     "grades": null,
#     "sympathy": false,
#     "antipathy": false,
#     "snsList": null,
#     "metaInfo": null,
#     "extension": null,
#     "audioInfoList": null,
#     "translation": null,
#     "report": null,
#     "middleBlindReport": false,
#     "spamInfo": null,
#     "userHomepageUrl": null,
#     "defamation": false,
#     "hiddenByCleanbot": false,
#     "visible": true,
#     "serviceId": null,
#     "idNo": "uOuY",
#     "manager": false,
#     "deleted": false,
#     "blindReport": false,
#     "anonymous": false,
#     "expose": true,
#     "blind": false,
#     "secret": false,
#     "profileUserId": null,
#     "containText": true,
#     "userBlocked": false,
#     "exposeByCountry": false,
#     "virtual": false,
#     "maskedUserId": "heez****",
#     "maskedUserName": "he****",
#     "validateBanWords": false
# }
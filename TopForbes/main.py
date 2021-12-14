import urllib
import json
from urllib import request

headers = {'cookie': 'notice_gdpr_prefs'}  # required cookie that needs to be sent to view the data

url_forbes = r"https://www.forbes.com/forbesapi/person/billionaires/2021/position/true.json?limit=100"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        req = urllib.request.Request(url_forbes, None, headers)
        resp = urllib.request.urlopen(req)
        data = resp.read().decode('utf-8')
        json_obj = json.loads(data)
        print(json_obj)
    except Exception as e:
        print("Error : ", e)

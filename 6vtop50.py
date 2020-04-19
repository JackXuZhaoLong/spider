import requests
import re
from requests.exceptions import RequestException
def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
        }
        response = requests.get(url, headers = headers)
        #print(response.encoding)
        response.encoding ='utf-8'
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None
def parse_page():
    url = 'https://www.66s.cc/qian50m.html'
    html = get_one_page(url)
    pattern = re.compile('<li><.*?>(.*?)</a></li>',re.S)
    res = re.findall(pattern, html)
    print(type(res))
    res = res[1:]
    for it in res:
        print(it)
parse_page()


import requests
import re
from multiprocessing import Pool
from requests.exceptions import RequestException

def get_response(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        # print(response.encoding)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None

def get_info(html):
    patten = re.compile('<td align="center">(.*?)<.*?<td class="al"><a.*?>(.*?)</a></td>.*?<td>(.*?)</td>',re.S)
    res = re.findall(patten,html)
    #print(res)
    for it in res:
        yield {
            'index': it[0],
            'content': it[1],
            'hot': it[2]
        }
def main(url):
    html = get_response(url)
    for item in get_info(html):
        print(item)

if __name__ == '__main__':
    url = 'https://tophub.today/n/mproPpoq6O'
    main(url)


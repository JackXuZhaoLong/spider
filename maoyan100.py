import requests
from requests.exceptions import RequestException
from multiprocessing import Pool
import  re
import json
import tkinter as tk


#获取单页的html
def get_one_page(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}
        response = requests.get(url, headers = headers)
        if response.status_code == 200:#判断是否请求成功
            return response.text
        return None
    except RequestException:
        return None
def parse_one_page(html):    #正则匹配获取关键信息
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern,html)
    for item in items:#此处如果返回一个字典则会占用内存，yield修饰的函数成为一个迭代器，可理解为中断，每次运行到yield则返回一个迭代器
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5]+item[6]
        }
def write_to_file(dict):
    with open('results.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(dict, ensure_ascii=False)+'\n')#json.dumps将字典转化为str
        f.close()

def ParseWeb(offset):
    url = 'https://maoyan.com/board/4?offset='+ str(offset)
    html = get_one_page(url)
    print(html)
    for item in parse_one_page(html):
        write_to_file(item)

if __name__ == '__main__':
    #单线程
    for i in range(10):
       ParseWeb(i*10)
    #多线程
#    pool = Pool()
#    pool.map(ParseWeb,[i*10 for i in range(10)])

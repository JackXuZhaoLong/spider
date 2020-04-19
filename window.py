import requests
from requests.exceptions import RequestException
from multiprocessing import Pool
import  re
import json
import tkinter as tk
from tkinter import  *


class MaoyanTop100():
    def __init__(self):
        self.window = tk.Tk()
        self.window.minsize(600, 800)
        self.window.title('猫眼Top100')
        label = tk.Label(self.window, text='猫眼热榜Top100', font=('黑体', 15))
        label.pack()
        s = Scrollbar(self.window)
        s.pack(side=RIGHT, fill=Y)
        self.text = tk.Text(self.window, width=100, height=60)
        self.text.pack()
        s.config(command=self.text.yview)
        self.text.config(yscrollcommand=s.set)
        button = tk.Button(self.window, text='查询', width=10, command = self.start)
        button.pack()
        button1 = tk.Button(self.window, text = '退出', width = 10, command = self.quite)
        button1.pack(anchor = 'se',padx = 160, pady = 10)
        # 多线程
        #    pool = Pool()
        #    pool.map(ParseWeb,[i*10 for i in range(10)])
        self.window.mainloop()

        # 获取单页的html
    def get_one_page(self,url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:  # 判断是否请求成功
                return response.text
            return None
        except RequestException:
            return None

    def parse_one_page(self,html):  # 正则匹配获取关键信息
        pattern = re.compile(
            '<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',
            re.S)
        items = re.findall(pattern, html)
        for item in items:  # 此处如果返回一个字典则会占用内存，yield修饰的函数成为一个迭代器，可理解为中断，每次运行到yield则返回一个迭代器
            yield {
                'index': item[0],
                'image': item[1],
                'title': item[2],
                'actor': item[3].strip()[3:],
                'time': item[4].strip()[5:],
                'score': item[5] + item[6]
            }
    def write_to_text(self,dict):
        info = dict['index']+' '+dict['title']+' '+dict['actor']+' '+dict['time']+' '+dict['score']+'\n'
        self.text.insert('insert',info)

    def ParseWeb(self,offset):
        url = 'https://maoyan.com/board/4?offset='+ str(offset)
        html = self.get_one_page(url)
        for item in self.parse_one_page(html):
            self.write_to_text(item)
    def start(self):
        #单线程
        for i in range(10):
           self.ParseWeb(i*10)
    def quite(self):
        self.window.quit()


MaoyanTop100().start()

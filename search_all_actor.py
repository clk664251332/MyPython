import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
import pandas as pd
import os


CONFIG = [
    {
        'name': 'wankzvr',
        'url': r"https://www.wankzvr.com/pornstars?p={}",
        'page': 1,
        'tag': 'a',
        'class': 'teaser__title'
    },
    {
        'name': 'vrbangers',
        'url': r"https://vrbangers.com/models/?page={}",
        'page': 1,
        'tag': 'div',
        'class': 'models-item__text w-100 z-index-3 text-center d-flex align-items-center justify-content-center'
    },
    {
        'name': 'realjamvr',
        'url': r"https://realjamvr.com/actors/?page={}",
        'page': 1,
        'tag': 'a',
        'class': 'panel-title'
    },
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

TARGET_FILE = "all_actor.txt"
write_file = open(TARGET_FILE, "w", encoding="utf-8")


def Request(url):
    req = urllib.request.Request(url=url, headers=headers, method="GET")
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    return html


def ExtractData(html, tag, class_name):
    bs = BeautifulSoup(html, "html.parser")
    t_list = bs.find_all(tag, class_=class_name)  # 这个class会和python冲突，所以后面加个下划线
    for element in t_list:
        str = (element.text.strip())
        print(str)
        write_file.writelines(str+'\n')


for web_config in CONFIG:
    str = "\n------"+web_config['name']+'------\n'
    print(str)
    write_file.writelines(str)

    all_page = web_config['page'] + 1
    for i in range(1, all_page):
        url = web_config['url'].format(i)
        try:
            html = Request(url)
        except urllib.error.URLError as e:
            print(e)
            continue
        ExtractData(html, web_config['tag'], web_config['class'])

write_file.close()
os.system("pause")

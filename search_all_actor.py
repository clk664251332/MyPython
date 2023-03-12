import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
import pandas as pd
import os
from io import BytesIO
import gzip

FILE_CONFIG = [
    {
        'name': 'DeepInSexVR',
        'path': 'webpage\deep_in_sex_list.txt',
        'tag': 'a',
        'class': 'white-link'
    },
    {
        'name': 'VirtualRealPorn',
        'path': 'webpage\Models - VirtualRealPorn.com.txt',
        'tag': 'h3',
        'class': '',
        'regex_sub': ' VR'
    },
    {
        'name': 'NaughtyAmericaVR',
        'path': r'webpage\Naughty_America.txt',
        'compile': r'https://www.naughtyamericavr.com/pornstar/',
    },
    {
        'name': 'SexBabesVR',
        'path': r'webpage\VR Girls_ Download VR Porn Girls Videos _ SexBabesVR.txt',
        'tag': 'h2',
        'class': ''
    },
]

CONFIG = [
    {
        'name': 'wankzvr',
        'url': r"https://www.wankzvr.com/pornstars?p={}",
        'page': 35,
        'tag': 'a',
        'class': 'teaser__title'
    },
    {
        'name': 'vrbangers',
        'url': r"https://vrbangers.com/models/?page={}",
        'page': 7,
        'tag': 'div',
        'class': 'models-item__text w-100 z-index-3 text-center d-flex align-items-center justify-content-center'
    },
    {
        'name': 'realjamvr',
        'url': r"https://realjamvr.com/actors/?page={}",
        'page': 28,
        'tag': 'a',
        'class': 'panel-title'
    },
    {
        'name': 'vrlatina',
        'url': r"https://vrlatina.com/models/page{}.html",
        'page': 6,
        'tag': 'span',
        'class': 'item-name'
    },
    # {
    #     'name': 'sexlikereal',
    #     'url': r"https://www.sexlikereal.com/pornstars?page={}",
    #     'page': 171,
    #     'tag': 'span',
    #     'class': 'item-name'
    # },
    {
        'name': 'vrhush',
        'url': r"https://vrhush.com/models?page={}",
        'page': 12,
        'tag': 'div',
        'class': 'name-wrapper',
        'deep':[1, 0, 0]
    },
    {
        'name': 'lethalhardcorevr',
        'url': r"https://www.lethalhardcorevr.com/lethal-hardcore-vr-the-porn-stars.html?page={}&hybridview=member",
        'page': 5,
        'tag': 'span',
        'class': 'overlay-inner'
    },
    {
        'name': 'sinsvr',
        'url': r"https://xsinsvr.com/models/sort/trending/{}",
        'page': 16,
        'tag': 'h3',
        'class': 'models__name'
    },
    {
        'name': 'badoinkvr',
        'url': r"https://badoinkvr.com/vr-pornstars/{}",
        'page': 40,
        'attrs': {"itemprop": "name"}
    },
    {
        'name': 'taboovrporn',
        'url': r"https://taboovrporn.com/models/models_{}.html",
        'page': 4,
        'tag': 'div',
        'class': 'model',
        'deep': [3, 1, 0]
    },
    {
        'name': 'vrconk',
        'url': r"https://vrconk.com/models/?page={}",
        'page': 10,
        'attrs': {"data-testid": "model-item-name"}
    },
    {
        'name': 'realitylovers',
        'url': r"https://realitylovers.com/girls/page{}",
        'page': 30,
        'tag': 'h2',
        'class': 'girlsCategory-girlName'
    },
    {
        'name': 'stripzvr',
        'url': r"https://www.stripzvr.com/p{}/",
        'page': 19,
        'attrs': {"target": "_self"},
        'gzip' : True
    },
    {
        'name': '18vr',
        'url': r"https://18vr.com/vrgirls/{}",
        'page': 21,
        'attrs': {"itemprop": "name"}
    },
    {
        'name': 'czechvr',
        'path': r'webpage\czechvr.txt',
        'tag': 'h2',
        'class': '',
        'deep' : [0,0]
    },
    {
        'name': 'tmwvrnet',
        'url': r"https://tmwvrnet.com/models/models_{}.html",
        'page': 8,
        'tag': 'h5',
        'class': 'thumbs__info__title'
    },
    {
        'name': 'vrcosplayx',
        'url': r"https://vrcosplayx.com/cosplaygirls/{}",
        'page': 20,
        'attrs': {"itemprop": "name"}
    },
]

TEST = [
    {
        'name': 'wetvr',
        'url': r'https://wetvr.com/girls?page={}',
        'page': 8,
        'tag': 'h5',
        'class': 'card-title',
    },
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

TARGET_FILE = "all_actor.txt"

def Request(url):
    req = urllib.request.Request(url=url, headers=headers, method="GET")
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    return html

def RequestWithGzip(url):
    req = urllib.request.Request(url=url, headers=headers, method="GET")
    response = urllib.request.urlopen(req)
    html = response.read()
    buff = BytesIO(html)
    f = gzip.GzipFile(fileobj=buff)
    html = f.read().decode('utf-8')
    return html

#从HTML中提取数据
def ExtractFromHtml(html):
    soup = BeautifulSoup(html, "html.parser")    
    str_list = []

    if 'class' in web_config:
        data_list = soup.find_all(web_config['tag'], class_=web_config['class'])
    elif 'attrs' in web_config:
        data_list = soup.find_all(attrs = web_config['attrs'])
    elif 'compile' in web_config:
        data_list = soup.find_all(href=re.compile(web_config['compile']))
    
    for element in data_list:
        if 'deep' in web_config:
            str = element
            for index in web_config['deep']:
                str = str.contents[index]
            str = str.strip()
        else:
            str = (element.contents[0].strip())

        if 'regex_sub' in web_config: #删除匹配文字
            str = re.sub(web_config['regex_sub'], "", str)
        if str == '':
            continue

        print(str)
        write_file.writelines(str+'\n')




#-----------------------程序开始-----------------------------------
write_file = open(TARGET_FILE, "w", encoding="utf-8")

for web_config in TEST:
    str = "\n------"+web_config['name']+'------\n'
    print(str)
    write_file.writelines(str)
    if 'path' in web_config:
        file = open(web_config['path'], encoding="utf-8")
        html = file.read()
        ExtractFromHtml(html)
    elif 'url' in web_config:
        all_page = web_config['page'] + 1
        for i in range(1, all_page):
            url = web_config['url'].format(i)
            try:
                if 'gzip' in web_config:
                    html = RequestWithGzip(url)
                else:
                    html = Request(url)
            except urllib.error.URLError as e:
                print(e)
                continue
            ExtractFromHtml(html)

write_file.close()
os.system("pause")

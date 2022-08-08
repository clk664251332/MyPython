import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
import pandas as pd
import os

URL = r"https://stasyqvr.com/virtualreality/list/page/{}"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

movie_names = []
actor_names = []
pages = []

#请求并返回html数据
def Request(url):
    req = urllib.request.Request(url=url, headers=headers, method="GET")
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    return html

#从html数据中提取想要的数据
def ExtractData(html, page):
    bs = BeautifulSoup(html, "html.parser")
    t_list = bs.find_all("div", class_="grid-info-inner") #这个class会和python冲突，所以后面加个下划线
    for element in t_list:
        element = str(element)
        bs = BeautifulSoup(element, "html.parser")
        movie_name_result_list = bs.select("div > a > h2")
        actor_name_result_list = bs.select("div > span > a")
        movie_name_result = movie_name_result_list[0].get_text()

        actor_name_result = ""
        for i in range(0, len(actor_name_result_list)):
            if i != len(actor_name_result_list)-1:
                actor_name_result = actor_name_result + actor_name_result_list[i].get_text() + " & "
            else:
                actor_name_result = actor_name_result + actor_name_result_list[i].get_text()

        movie_names.append(movie_name_result)
        actor_names.append(actor_name_result)
        pages.append(page)

        print(actor_name_result + " - " + movie_name_result)

def SaveData():
    data = {
        'Movie':movie_names,
        'Actor':actor_names,
        'Page':pages
    }
    df = pd.DataFrame(data)
    df.to_csv('StasyQvr演员表.csv', index=False, encoding='utf-8')


for i in range(1, 44):
    url = URL.format(i)
    try:
        html = Request(url)
    except urllib.error.URLError as e:
         print(e)
         continue
    print("----第{0}页----".format(i))
    ExtractData(html, i)     
    SaveData()

os.system("pause")
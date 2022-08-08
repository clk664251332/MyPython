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

find_movie_name = re.compile(r"<h2>(.*?)<\/h2>")
find_actor_name = re.compile(r"<a href=(.*?)>(.*)<\/a> <\/span>")

movie_names = []
actor_names = []

#请求并返回html数据
def Request(url):
    req = urllib.request.Request(url=url, headers=headers, method="GET")
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    return html

#从html数据中提取想要的数据
def ExtractData(html):
    bs = BeautifulSoup(html, "html.parser")
    t_list = bs.find_all("div", class_="grid-info-inner") #这个class会和python冲突，所以后面加个下划线
    for element in t_list:
        element = str(element)
        movie_find_result = re.findall(find_movie_name, element)
        actor_find_result = re.findall(find_actor_name, element)
        movie_name_result = "NA"
        actor_name_result = "NA"
        if len(movie_find_result) == 0 or len(actor_find_result) == 0:
            pass
        else:
            movie_name_result = movie_find_result[0]
            actor_name_result = actor_find_result[0][1]

        movie_names.append(movie_name_result)
        actor_names.append(actor_name_result)

        print(actor_name_result + " - " + movie_name_result)

def SaveData():
    data = {
        'Movie':movie_names,
        'Actor':actor_names,
    }
    df = pd.DataFrame(data)
    df.to_csv('StasyQvr演员表.csv', index=False, encoding='utf-8')


for i in range(17, 44):
    url = URL.format(i)
    try:
        html = Request(url)
    except urllib.error.URLError as e:
         print(e)
         continue
    print("----第{0}页----".format(i))
    ExtractData(html)     
    SaveData()

os.system("pause")
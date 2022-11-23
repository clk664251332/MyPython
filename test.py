import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
import pandas as pd
import os


URL = r"http://www.youdao.com/w/eng/water"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}
PHONETIC_PATTERN = r"\[.*\]"

def Request(url):
    req = urllib.request.Request(url=url, headers=headers, method="GET")
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    bs = BeautifulSoup(html, "html.parser")
    t_list = bs.find_all("div", class_="baav")
    return t_list[len(t_list) - 1]



#test = "<span class=\"phonetic\">[ˈwɔːtə(r)]</span>"

string_result = str(Request(URL))
#result = re.findall(PHONETIC_PATTERN, string_result)
print(string_result)
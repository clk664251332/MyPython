import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
import pandas as pd
import os


url = r"https://www.sexlikereal.com/pornstars?page=1"

test = '''
<h2 class="girlsCategory-girlName">Adelle Sabelle
    <span class="girlsCategory-numberOfVideos">1&nbsp;Video</span>
</h2>
'''
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

# def Request(url):
#     req = urllib.request.Request(url=url, headers=headers, method="GET")
#     response = urllib.request.urlopen(req)
#     html = response.read().decode("utf-8")
#     return html

# html = Request(url)
# print(html)

# bs = BeautifulSoup(test, "html.parser")
# t_list = bs.find_all('h2', class_="girlsCategory-girlName")
# for element in t_list:
#     print(element.contents[0].strip()) #输出元素

str = 'Scarlett Jones VR'
print(re.sub(' VR', '', str))
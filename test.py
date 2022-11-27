import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
import pandas as pd
import os

URL = r"http://www.youdao.com/w/eng/{0}"
HEADERS = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

def RequestPhoneticSymbol(word):
    reqUrl = URL.format(word)
    req = urllib.request.Request(url=reqUrl, headers=HEADERS, method="GET")
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    print(html)

RequestPhoneticSymbol("isn't it?")
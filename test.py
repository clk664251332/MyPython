import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
import pandas as pd
import os

YINBIAO_PATTERN = r"\[.+\]"
line = "**<div style='text-align:center'><h1>punctual</h1></div><div style='text-align:center; font-size:85%;'><span style='font-family: Arial; color:blue;'>[ˈpʌŋktʃuəl]</span></div>"
yinbiao = re.findall(YINBIAO_PATTERN, line)

print("***clk&"[3:-1])
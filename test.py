import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
import pandas as pd
import os

string = "square footage		直译：平方英尺，意思就是“面积”		"
list = string.split('\t')
list[1] = "[li si te]"
new_string = '\t'.join(list)
print(new_string)
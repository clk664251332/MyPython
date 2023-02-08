import os
import re
import urllib
import urllib.request
from bs4 import BeautifulSoup

#SOURCE_FILE = "text.txt"
SOURCE_FILE = "选中的笔记.txt"
TARGET_FILE = "选中的笔记_增加音标.txt"

PHONETIC_PATTERN = r"\[.*\]"
KANJI_PATTERN = r"[\u4e00-\u9fa5]+"

URL = r"http://www.youdao.com/w/eng/{0}"
HEADERS = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

read_file = open(SOURCE_FILE, "r", encoding="utf-8")
write_file = open(TARGET_FILE, "w", encoding="utf-8")

#从网络获取音标
def RequestPhoneticSymbol(word):
    reqUrl = URL.format(word)
    try:
        req = urllib.request.Request(url=reqUrl, headers=HEADERS, method="GET")
        response = urllib.request.urlopen(req)
    except:
        #print(str.format("网络获取单词{0}音标失败，原因为{1}", word, e))
        return "" 
    html = response.read().decode("utf-8")
    bs = BeautifulSoup(html, "html.parser")
    t_list = bs.find_all("div", class_="baav")
    if len(t_list) <=0:
        #print(word + " 没有查到音标")
        return "" 
    result = str(t_list[len(t_list) - 1])
    extracted_result = re.findall(PHONETIC_PATTERN, result)
    length = len(extracted_result)
    if length>0:
        return extracted_result[length -1]
    else:
        #print(result + "，没有提取出音标")
        return ""

#对读取的每一行进行处理
def ProcessLine(line):
    list = line.split('\t')
    word = list[0]
    word_list = word.split(' ')
    if len(word_list) > 1:
        kanji = re.findall(KANJI_PATTERN, word)
        if len(kanji) > 0:
            return line
        yin_biao = RequestPhoneticSymbol(word)
        if yin_biao == "":
            return line
        list[1] = yin_biao
        print("单词%s新增音标", word)
        return '\t'.join(list)
    else:
        return line


read_content = read_file.readlines()
for read_line in read_content:
    result = ProcessLine(read_line) #处理每一行
    write_file.writelines(result) #处理的结果写入新文件中

read_file.close()
write_file.close()

os.system("pause")
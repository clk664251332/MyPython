#处理英语单词笔记
##print("  asad  ".strip())

#处理每一行（去除空格，去除音标）
#第一行 标题
#第二行 单词
#第三行 释义
#后面每一行都是拓展
#检测到空行 该区域解析完成
import re
import urllib
import urllib.request
from bs4 import BeautifulSoup

SOURCE_FILE = "vocabulary_test.txt"
TARGET_FILE = "vocabulary_new.txt"
PATTERN = r"\[[^\u4e00-\u9fa5]*?\]"
PHONETIC_PATTERN = r"\[.*\]"
Title_Replace = "*{0}\n**<div style='text-align:center'><h1>{1}</h1></div><div style='text-align:center; font-size:85%;'><span style='font-family: Arial; color:blue;'>{2}</span></div>\n"
Paraphrase_Replace = '***{0}\n<hr style="height:1px;border:none;border-top:1px dashed #0066CC;background-color:#ffffff;">\n'
URL = r"http://www.youdao.com/w/eng/{0}"
HEADERS = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

line_count = 0
all_count = 0
current_vob = ""

#处理掉字符串前后空格和音标
def Strip(line):
    line = re.sub(PATTERN, "", line)
    return line.strip()

#从网络获取音标
def RequestPhoneticSymbol(world):
    reqUrl = URL.format(world)
    req = urllib.request.Request(url=reqUrl, headers=HEADERS, method="GET")
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    bs = BeautifulSoup(html, "html.parser")
    t_list = bs.find_all("div", class_="baav")
    if len(t_list) <=0:
        print(world + " 没有查到音标")
        return "" 
    result = str(t_list[len(t_list) - 1])
    extracted_result = re.findall(PHONETIC_PATTERN, result)
    length = len(extracted_result)
    if length>0:
        return extracted_result[length -1]
    else:
        print(result + "，没有提取出音标")
        return ""

#获取音标
def GetPhoneticSymbol(word):
    count = len(str.split(word, ' '))
    if count > 1: #词组不查找音标
        return ""
    else:
        try:
            return RequestPhoneticSymbol(word)
        except urllib.error.URLError as e:
            print(str.format("网络获取单词{0}音标失败，原因为{1}", word, e))
            return ""

#对读取的每一行进行处理
def ProcessLine(line):
    global line_count
    if line == '\n':
        line_count = 0
    else:
        line_count = line_count + 1 #行数+1
        line = Strip(line)

    if line_count == 0:
        pass
    elif line_count == 1:
        line = ProcessTitle(line)
    elif line_count == 2:
        line = ProcessParaphrase(line)
    elif line_count == 3:
        line = ProcessExample(line)
    return line

#处理标题
def ProcessTitle(line):
    print("正在处理 " + line)
    global all_count
    global current_vob
    current_vob = line
    all_count = all_count + 1
    #line = "标题：" + line
    phonetic_symbol = GetPhoneticSymbol(line)
    return Title_Replace.format(line, line, phonetic_symbol)

#处理释义
def ProcessParaphrase(line):
    #line = "释义：" + line
    return Paraphrase_Replace.format(line)

#处理例句
def ProcessExample(line):
    line = line + "\n"
    line = AddOther(line)
    line = AddAudio(line)
    return line

#添加中间的部分
def AddOther(content):
    for i in range(4, 9):
        content = content + '*'*i + '\n'
    return content

#添加最后的语音
def AddAudio(content):
    return content + '*' * 9 + '\n'

def Main():
    read_file = open(SOURCE_FILE, "r", encoding="utf-8")
    write_file = open(TARGET_FILE, "w", encoding="utf-8")

    read_content = read_file.readlines()
    for read_line in read_content:
        result = ProcessLine(read_line) #处理每一行
        write_file.writelines(result) #处理的结果写入新文件中

    read_file.close()
    write_file.close()

Main()
print("处理完毕，共计数量" + str(all_count))
#处理英语单词笔记
##Log("  asad  ".strip())

#处理每一行（去除空格，去除音标）
#第一行 标题
#第二行 单词
#第三行 释义
#后面每一行都是拓展
#检测到空行 该区域解析完成
import os
import re
import urllib
import urllib.request
from bs4 import BeautifulSoup

SOURCE_FILE = "vocabulary.txt"
TARGET_FILE = "vocabulary_output.txt"
LOG_FILE = "vocabulary_log.txt"
PATTERN = r"\[[^\u4e00-\u9fa5]*?\]"
PHONETIC_PATTERN = r"\[.*\]"
KANJI_PATTERN = r"[\u4e00-\u9fa5]+"
Title_Replace = "*{0}\n**<div style='text-align:center'><h1>{1}</h1></div><div style='text-align:center; font-size:85%;'><span style='font-family: Arial; color:blue;'>{2}</span></div>\n"
Paraphrase_Replace = '***{0}\n<hr style="height:1px;border:none;border-top:1px dashed #0066CC;background-color:#ffffff;">\n'
URL = r"http://www.youdao.com/w/eng/{0}"
HEADERS = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

g_line_count = 0
g_all_count = 0
g_current_word = ""
g_progress = 0
g_log_file = 0

def Log(content):
    global g_log_file
    g_log_file.writelines(content + '\n')
    print(content)

#处理掉字符串前后空格和音标
def Strip(line):
    line = re.sub(PATTERN, "", line)
    return line.strip()

#从网络获取音标
def RequestPhoneticSymbol(word):
    reqUrl = URL.format(word)
    try:
        req = urllib.request.Request(url=reqUrl, headers=HEADERS, method="GET")
        response = urllib.request.urlopen(req)
    except urllib.error.URLError as e:
        Log(str.format("网络获取单词{0}音标失败，原因为{1}", word, e))
        return "" 
    html = response.read().decode("utf-8")
    bs = BeautifulSoup(html, "html.parser")
    t_list = bs.find_all("div", class_="baav")
    if len(t_list) <=0:
        Log(word + " 没有查到音标")
        return "" 
    result = str(t_list[len(t_list) - 1])
    extracted_result = re.findall(PHONETIC_PATTERN, result)
    length = len(extracted_result)
    if length>0:
        return extracted_result[length -1]
    else:
        Log(result + "，没有提取出音标")
        return ""

#获取音标
def GetPhoneticSymbol(word):
    kanji = re.findall(KANJI_PATTERN, word)
    if len(kanji):
        return ""
    count = len(str.split(word, ' '))
    if count > 1: #词组不查找音标
        return ""
    else:
        return RequestPhoneticSymbol(word)

#对读取的每一行进行处理
def ProcessLine(line):
    global g_line_count
    line = Strip(line)
    if line == '':
        if g_line_count != 0:
            line = ProcessBlankLine()
        g_line_count = 0
    else:
        g_line_count = g_line_count + 1 #行数+1

    if g_line_count == 0:
        pass
    elif g_line_count == 1:
        line = ProcessTitle(line)
    elif g_line_count == 2:
        line = ProcessParaphrase(line)
    elif g_line_count >= 3:
        line = ProcessExample(line)
    return line

#处理标题
def ProcessTitle(line):
    Log(str.format("({0:.1%})正在处理 {1}", g_progress, line))
    global g_all_count
    global g_current_word
    g_current_word = line
    g_all_count = g_all_count + 1
    phonetic_symbol = GetPhoneticSymbol(line)
    #phonetic_symbol = ''
    return Title_Replace.format(line, line, phonetic_symbol)

#处理释义
def ProcessParaphrase(line):
    return Paraphrase_Replace.format(line)

#处理例句
def ProcessExample(line):
    return line + "\n"

#处理空行
def ProcessBlankLine():
    return AddOther() + AddAudio() + '\n'

#添加中间的部分
def AddOther():
    content = ""
    for i in range(4, 9):
        content = content + '*'*i + '\n'
    return content

#添加最后的语音
def AddAudio():
    content = ""
    return content + '*' * 9 + '\n'

def Main():
    global g_progress
    global g_log_file
    read_file = open(SOURCE_FILE, "r", encoding="utf-8")
    write_file = open(TARGET_FILE, "w", encoding="utf-8")
    g_log_file = open(LOG_FILE, "w", encoding="utf-8")

    read_content = read_file.readlines()
    all_line_count = len(read_content)
    lint_count = 0
    for read_line in read_content:
        lint_count = lint_count + 1
        g_progress = lint_count / all_line_count
        result = ProcessLine(read_line) #处理每一行
        write_file.writelines(result) #处理的结果写入新文件中

    read_file.close()
    write_file.close()

Main()
Log("\n处理完毕，共计数量 " + str(g_all_count))
g_log_file.close()

os.system("pause")
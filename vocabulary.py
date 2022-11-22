#处理英语单词笔记
##print("  asad  ".strip())

#处理每一行（去除空格，去除音标）
#第一行 标题
#第二行 单词
#第三行 释义
#后面每一行都是拓展
#检测到空行 该区域解析完成
import re

SOURCE_FILE = "vocabulary_test.txt"
TARGET_FILE = "vocabulary_new.txt"
PATTERN = r"\[[^\u4e00-\u9fa5]*?\]"
Title_Replace = "*{0}\n**<div style='text-align:center'><h1>{1}</h1></div><div style='text-align:center; font-size:85%;'><span style='font-family: Arial; color:blue;'>{2}</span></div>\n"
Paraphrase_Replace = '***{0}\n<hr style="height:1px;border:none;border-top:1px dashed #0066CC;background-color:#ffffff;">\n'
line_count = 0
all_count = 0
current_vob = ""

#处理掉字符串前后空格和音标
def Strip(line):
    line = re.sub(PATTERN, "", line)
    return line.strip()

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
    global all_count
    global current_vob
    current_vob = line
    all_count = all_count + 1
    #line = "标题：" + line
    return Title_Replace.format(line, line, current_vob + "的音标")

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
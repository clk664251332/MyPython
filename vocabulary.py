#处理英语单词笔记
##print("  asad  ".strip())

#处理每一行（去除空格，去除音标）
#第一行 标题
#第二行 单词
#第三行 释义
#后面每一行都是拓展
#检测到空行 该区域解析完成
import re

SOURCE_FILE = "vocabulary.txt"
TARGET_FILE = "vocabulary_new.txt"
PATTERN = r"\[[^\u4e00-\u9fa5]*?\]"
line_count = 0
all_count = 0


#处理掉字符串前后空格和音标
def Strip(line):
    line = re.sub(PATTERN, "", line)
    return line.strip() + '\n'

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
    
    return line

#处理标题
def ProcessTitle(line):
    global all_count
    all_count = all_count + 1
    #line = "标题：" + line
    return line

#处理释义
def ProcessParaphrase(line):
    #line = "释义：" + line
    return line

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
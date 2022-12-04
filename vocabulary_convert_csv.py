#提取出 单词、音标、意思、例句
import pandas as pd
import os
import re

SOURCE_FILE = "vocabulary_output.txt"
TARGET_FILE = "vocabulary_output_new.txt"

YINBIAO_PATTERN = r"\[.+\]"

danci_list = []
yinbiao_list = []
yisi_list = []
liju_list = []

g_line_count = 0
g_cur_liju = ""

def extarct_danci(content):
    pass

def extarct_yinbiao(content):
    pass

def extarct_yisi(content):
    pass

def extarct_liju(content):
    pass

def ProcessLine(line):
    global g_line_count
    global g_cur_liju
    g_line_count = g_line_count + 1
    if line == '\n':
        g_line_count = 0
        liju_list.append(g_cur_liju[:-1])
        g_cur_liju = ''
        return

    if g_line_count == 1:
        danci_list.append(line[1:-1])
    elif g_line_count == 2:
        yinbiao = re.findall(YINBIAO_PATTERN, line)
        if len(yinbiao) > 0:
            yinbiao_list.append(yinbiao[0])
        else:
            yinbiao_list.append(' ')
    elif g_line_count == 3:
        yisi_list.append(line[3:-1])
    elif g_line_count == 4:
        pass
    elif not line.startswith('*'):
        g_cur_liju = g_cur_liju + line

read_file = open(SOURCE_FILE, "r", encoding="utf-8")
#write_file = open(TARGET_FILE, "w", encoding="utf-8")
read_content = read_file.readlines()
for read_line in read_content:
    # if read_line.startswith('*'):
    #     extarct_danci(read_line)
    # elif read_line.startswith('**'):
    #     extarct_yinbiao(read_line)
    # elif read_line.startswith('***'):
    #     extarct_yisi(read_line)
    ProcessLine(read_line)
    #write_file.writelines(result)

read_file.close()
#write_file.close()

data = {
    'danci':danci_list,
    'yinbiao':yinbiao_list,
    'yisi':yisi_list,
    'liju':liju_list,
}
df = pd.DataFrame(data)
df.to_csv('import.csv', index=False, encoding='utf-8-sig')
os.system("pause")
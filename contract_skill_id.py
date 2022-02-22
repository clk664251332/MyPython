###生成一份原技能id与缩短后技能id的映射
from telnetlib import theNULL
import pandas as pd
import os

CSV_PATH = "./CSV/SkillTable.csv"
CONTRACT_TABLE = {}
INDEX = 0

#递归处理数值，figure是从后往前数需要改变的位数
def change_number_recursion(origin, number, figure):
    global CONTRACT_TABLE
    add_count_max = False
    #101501 -> 111501(figure = 5)
    while(str(number) in CONTRACT_TABLE):
        figure_value = str(number)[-figure]
        if figure_value == '9':
            add_count_max = True
            break
        number += 10**(figure-1)
    
    if add_count_max:
        figure -= 1
        if figure <=0:
            print("失败{0}值变成了{1}".format(origin, str(number)))
            return
        number = change_number_recursion(origin, number, figure)

    #CONTRACT_TABLE[str(number)] = pd.to_numeric(origin)
    return number

def contract_and_record(value):
    global CONTRACT_TABLE
    global INDEX
    init = value[0:1]
    after_str = value[5:]
    ret = init + after_str
    if ret not in CONTRACT_TABLE:
        CONTRACT_TABLE[ret] = pd.to_numeric(value)
    else:
        #删除1-4位不行，尝试第2位+1
        if value == '1004091901':
            pass
        end = change_number_recursion(value, pd.to_numeric(ret), 5)
        if str(end) not in CONTRACT_TABLE:
            CONTRACT_TABLE[str(end)] = pd.to_numeric(value)
        # else:
        #     print("出错？333333")
        #print("重复:value {0}变{1}，原value={2}，最终改变为 {3}".format(value,ret,CONTRACT_TABLE[ret],end))

    #print(ret)
    # INDEX += 1
    # part = value[1:5]
    # after_value = value.replace(part, str(INDEX))
    # print("替换数字{0} = {1}".format(value, after_value))

def main():
    df = pd.read_csv(CSV_PATH).drop([0])
    filter_data = df.loc[df["Id"].str.len()>=10, "Id"]
    filter_data.apply(contract_and_record)
    #print(len(filter_data))
    #print(CONTRACT_TABLE)
main()
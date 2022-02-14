import pandas as pd
import os

CSV_PATH = "./CSV"
LUA_OUT_PATH = "./Out"
CONFIG = [
    ["SkillEffectTable.csv", "ConfirmScript"]
]

def is_number(s):
    try: 
        float(s)
        return True
    except ValueError: 
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def unpack_to_lists(value):
    vector = value.split('|')
    for i in range(len(vector)):
        sequence = vector[i].split('=')
        vector[i] = sequence
    return vector

#处理对应字段的每一个数值
def process_field_value(row, filed_name, file_stream):
    #print(row)
    lists = unpack_to_lists(row[filed_name])
    #解析函数名和参数，然后生成对应代码
    skill_id = row["Id"]
    func_name = lists[0][0]
    file_stream.writelines("\t[{0}]=\n\t{{\n".format(skill_id))
    file_stream.writelines("\t\tfuncname = \"{0}\",\n".format(func_name))
    file_stream.writelines('\t\targs=\n\t\t\t{\n')
    for i in range(1, len(lists)):
        k = lists[i][0]
        v = lists[i][1]
        if not is_number(v):
            file_stream.writelines("\t\t\t\t{{k=\"{0}\", v=\"{1}\"}},\n".format(k,v))
        else:
            file_stream.writelines("\t\t\t\t{{k=\"{0}\", v={1}}},\n".format(k,v))
    file_stream.writelines('\t\t\t}\n\t},\n')

def generate_lua(config_row):
    #解析配置
    file_path = os.path.join(CSV_PATH, config_row[0])
    filed_name = config_row[1]
    df = pd.read_csv(file_path).drop([0])
    filter_data = df.loc[(pd.isna(df[filed_name]) == False), ["Id","ConfirmScript"]]
    #print(filter_data)
    #创建文件
    lua_file_name = filed_name + "OldConfig"
    f = open(os.path.join(LUA_OUT_PATH, lua_file_name + ".lua"),"w")
    f.writelines("{0} = {{\n".format(lua_file_name))
    filter_data.apply(process_field_value, args=[filed_name, f], axis = 1)
    f.writelines('}')
    f.close()

def main():
    if not os.path.exists(LUA_OUT_PATH):
        os.mkdir(LUA_OUT_PATH)
    for config_row in CONFIG:
        ret = generate_lua(config_row)
        if not ret:
            continue
    os.system("pause")

main()
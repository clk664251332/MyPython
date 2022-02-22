###脚本作用：根据csv表的ConfirmScript字段生成一份lua配置
import pandas as pd
import os

CSV_PATH = "./CSV"
LUA_OUT_PATH = "./Out"
CONFIG = [
    ["SkillEffectTable.csv", "ConfirmScript"]
]
LUA_CLASS_STR = '''class("{0}")

function {0}:GetParam(key)
	return self.data[key]
end

function {0}:HasId(id)
	return self.DATAS[id] ~= nil
end

function {0}:GetConfig(id)
	if not self:HasId(id) then
		return false
	end

	self.data = self.DATAS[id]
	self.funcname = self.data.funcname
	return self
end\n\n'''

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
    lists = unpack_to_lists(row[filed_name])
    #解析函数名和参数，然后生成对应代码
    skill_id = row["Id"]
    func_name = lists[0][0]
    file_stream.writelines("\t[{0}]=\n\t{{\n".format(skill_id))
    file_stream.writelines("\t\tfuncname = \"{0}\",\n".format(func_name))
    file_stream.writelines("\t\targs =\n\t\t{\n")
    for i in range(1, len(lists)):
        k = lists[i][0]
        v = lists[i][1]
        if not is_number(v):
            file_stream.writelines("\t\t\t{0} = \"{1}\",\n".format(k,v))
        else:

            file_stream.writelines("\t\t\t{0} = {1},\n".format(k,v))
    file_stream.writelines('\t\t}\n\t},\n')

#生成lua类
def generate_lua_class(file_stream, filed_name):
    class_name = filed_name + "Tools"
    file_stream.writelines(LUA_CLASS_STR.format(class_name))

#读取csv获取字段数据并写入lua文件
def generate_lua_data(file_stream, csv_path, filed_name):
    df = pd.read_csv(csv_path).drop([0])
    filter_data = df.loc[(pd.isna(df[filed_name]) == False), ["Id","ConfirmScript"]]
    #print(filter_data)
    class_name = filed_name + "Config"
    file_stream.writelines("{0} = {{\n".format(class_name))
    filter_data.apply(process_field_value, args=[filed_name, file_stream], axis = 1)
    file_stream.writelines('}')

def main():
    if not os.path.exists(LUA_OUT_PATH):
        os.mkdir(LUA_OUT_PATH)
    for config_row in CONFIG:
        try:
            csv_path = os.path.join(CSV_PATH, config_row[0])
            filed_name = config_row[1]
            lua_file_name = filed_name + "OldConfig"
            #创建文件
            f = open(os.path.join(LUA_OUT_PATH, lua_file_name + ".lua"),"w")
            #generate_lua_class(f, filed_name)
            generate_lua_data(f, csv_path, filed_name)
            f.close()
        except Exception as e:
            print("导出文件{0}时出错，原因为：{1}".format(filed_name, str(e)))
            f.close()
            continue
    os.system("pause")

main()
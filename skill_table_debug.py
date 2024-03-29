##旧的effect表和skill表有些id没有双向关联起来，该脚本找到这些配错的id
##增加功能：现有SkillTable的GroupId字段替换成正确的
import pandas as pd
import os

SKILL_TABLE_PATH = "E:\\workspace3\\config\Table\\CSV\SkillTable.csv"
SKILL_EFFECT_TABLE_PATH = "E:\\workspace3\\config\Table\\CSV\\SkillEffectTable.csv"
PASSIVE_SKILL_EFFECT_TABLE_PATH = "E:\\workspace3\\config\\Table\\CSV\\PassivitySkillEffectTable.csv"
REPLACED_SKILL_TABLE_PATH = r"E:\workspace4\config\Table\CSV\SkillTable.csv"

skill_df = pd.read_csv(SKILL_TABLE_PATH)
skill_effect_df = pd.read_csv(SKILL_EFFECT_TABLE_PATH)
passive_skill_effect_df = pd.read_csv(PASSIVE_SKILL_EFFECT_TABLE_PATH)
replaced_skill_table_df = pd.read_csv(REPLACED_SKILL_TABLE_PATH)

skill_effect_df.set_index("Id", inplace=True)
passive_skill_effect_df.set_index("Id", inplace=True)
#replaced_skill_table_df.set_index("Id")

#替换字典 effect_id = 正确的技能id
replace_map = {}
#找到每个skillId的effectId列表
#在effect表中对比对应的skillId是不是这个

def VectorToTable(value):
    vector = value.split('|')
    return vector

def walk_through(value):
    global f, replace_map
    skill_id = value["Id"]
    effect_ids = value["EffectIDs"]
    if not pd.isna(effect_ids):
        effect_id_list = VectorToTable(effect_ids)
        for effect_id in effect_id_list:
            check_error1, check_error2 = False, False
            ret_skill_id = 0
            try:
                ret_skill_id = skill_effect_df.loc[effect_id, "SkillID"]
            except:
                check_error1 = True
            try:
                passive_skill_effect_df.loc[effect_id, "SkillLevel"]
            except:
                check_error2 = True
            if check_error1 and check_error2 == True:
                #f.writelines("effect表和passive_efefct都找不到id= {0} 对应skill表Id= {1}\n".format(effect_id, skill_id))
                continue
            
            if check_error1 == False:
                if ret_skill_id != skill_id:
                    #f.writelines("发现Id对不上的错误，skill_id= {0}, effect_id= {1}\n".format(skill_id, effect_id))
                    replace_map[effect_id] = ret_skill_id

#f = open("./error.txt","w")
skill_df.loc[1:,:].apply(walk_through, axis = 1)
#f.close()

#替换
#print(replaced_skill_table_df.head())
for key in replace_map:
    try:
        ret = replaced_skill_table_df.loc[replaced_skill_table_df["Id"]==key, "SkillGroupID"]
        test = replace_map[key]
        pass
        #print(ret)
        #replaced_skill_table_df.loc[replaced_skill_table_df["Id"]==key, "SkillGroupID"] = replace_map[key]
        #print(replaced_skill_table_df.loc[key, "SkillGroupID"])
    except Exception as e:
        #print("skillTable表中未找到id={0}".format(key))
        print("异常 "+str(e))
        continue

replaced_skill_table_df.to_csv(REPLACED_SKILL_TABLE_PATH, index=False, encoding="utf_8_sig")
os.system("pause")
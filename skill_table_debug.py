#旧的effect表和skill表有些id没有双向关联起来，该脚本找到这些配错的id
import pandas as pd
import os

SKILL_TABLE_PATH = "E:\workspace3\config\Table\CSV\SkillTable.csv"
SKILL_EFFECT_TABLE_PATH = "E:\workspace3\config\Table\CSV\SkillEffectTable.csv"
PASSIVE_SKILL_EFFECT_TABLE_PATH = "E:\workspace3\config\Table\CSV\PassivitySkillEffectTable.csv"

skill_df = pd.read_csv(SKILL_TABLE_PATH)
skill_effect_df = pd.read_csv(SKILL_EFFECT_TABLE_PATH)
passive_skill_effect_df = pd.read_csv(PASSIVE_SKILL_EFFECT_TABLE_PATH)
skill_effect_df.set_index("Id", inplace=True)
passive_skill_effect_df.set_index("Id", inplace=True)

#找到每个skillId的effectId列表
#在effect表中对比对应的skillId是不是这个

def VectorToTable(value):
    vector = value.split('|')
    return vector

def walk_through(value):
    global f
    skill_id = value["Id"]
    effect_ids = value["EffectIDs"]
    if not pd.isna(effect_ids):
        effect_id_list = VectorToTable(effect_ids)
        for effect_id in effect_id_list:
            check1, check2 = 0, 0
            ret = 0
            try:
                ret = skill_effect_df.loc[effect_id, "SkillID"]
            except:
                check1 = 1
            try:
                passive_skill_effect_df.loc[effect_id, "SkillLevel"]
            except:
                check2 = 1
            if check1 + check2 == 2:
                f.writelines("effect表+passive_efefct都找不到id= {0} 对应skill表Id= {1}\n".format(effect_id, skill_id))
                continue
            
            if check1 == 0:
                if ret != skill_id:
                    f.writelines("发现Id对不上的错误，skill_id= {0}, effect_id= {1}\n".format(skill_id, effect_id))

f = open("./error.txt","w")
skill_df.loc[1:,:].apply(walk_through, axis = 1)
f.close()

os.system("pause")
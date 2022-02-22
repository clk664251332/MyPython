###还原一些字段，从旧的skill_effect_table表中获取数据放到新的skillTable表中
import pandas as pd
import os

SKILL_TABLE_PATH = "E:\workspace4\config\Table\CSV\SkillTable.csv"
SKILL_EFFECT_TABLE_PATH = "E:/SkillEffectTable.csv"

skill_df = pd.read_csv(SKILL_TABLE_PATH)
skill_effect_df = pd.read_csv(SKILL_EFFECT_TABLE_PATH)
skill_effect_df.set_index("Id", inplace=True)

def get_prefix(value):
    skillId = value["Id"]
    try:
        ret = skill_effect_df.loc[skillId,"SkillScriptPrefix"]
    except:
        print("技能id为{0}没有对应的effect数据".format(skillId))
        return ''
    return ret

def get_postfix(value):
    skillId = value["Id"]
    try:
        ret = skill_effect_df.loc[skillId,"SkillScriptPostfix"]
    except:
        return ''
    return ret

skill_df.loc[:,"SkillScriptPrefix"] = skill_df.loc[1:,:].apply(get_prefix, axis = 1)
skill_df.loc[:,"SkillScriptPostfix"] = skill_df.loc[1:,:].apply(get_postfix, axis = 1)

skill_df.to_csv(SKILL_TABLE_PATH, index=False, encoding="utf_8_sig")

os.system("pause")
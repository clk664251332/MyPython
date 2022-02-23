###八SkillEffectTable的SkillID字段转移到新的SkillTable表中，新字段名字叫SkillGroupId
import pandas as pd
import os

SKILL_EFFECT_PATH = "./SkillEffectTable.csv"
TARGET_SKILL_TABLE = "./CSV/SkillTable_new.csv"

skill_effect_df = pd.read_csv(SKILL_EFFECT_PATH)
skill_target_df = pd.read_csv(TARGET_SKILL_TABLE)

skill_effect_df.set_index("Id", inplace=True)
#print(skill_map_df)

def GetOriginId(value):
    skillId = value["Id"]
    try:
        ret = skill_effect_df.loc[skillId, "SkillID"]
    except:
        print("技能id为 {0} 没有对应的原id".format(skillId))
        return skillId
    return ret

skill_target_df.loc[:, "SkillGroupID"] = skill_target_df.loc[1:,:].apply(GetOriginId, axis = 1)
skill_target_df.to_csv(TARGET_SKILL_TABLE, index=False, encoding="utf_8_sig")
os.system("pause")
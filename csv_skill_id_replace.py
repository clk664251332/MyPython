#脚本作用，把各表引用到skillId的地方转换成skillEffectId
from cmath import isnan
from pickle import TRUE
import pandas as pd
import os

CSV_PATH = "./CSV"
CSV_NEW_PATH = "./NewCSV/"
CREATE_NEW_FILE = False
SKILL_ID_COLUNM = None
SKILL_EFFECT_MAP = {}

def VectorToTable(value):
    vector = value.split('|')
    return vector

def unpack_to_lists(value):
    vector = value.split('|')
    for i in range(len(vector)):
        sequence = vector[i].split('=')
        vector[i] = sequence
    return vector

def pack_to_str(value):
    ret = ""
    for i in range(len(value)):
        sequence = value[i]
        for j in range(len(sequence)):
            if pd.isna(sequence[j]):
                continue
            ret = ret + str(sequence[j])
            if not j == len(sequence)-1:
                ret = ret + '='
        if not i == len(value)-1:
            ret = ret + '|'

    return ret

def get_effect_id(skill_id):
    if skill_id not in SKILL_EFFECT_MAP:
        print("出错，映射表中没有此id {0}对应的effectId".format(skill_id))
        return skill_id
    return SKILL_EFFECT_MAP[skill_id]
#============================替换函数 Start============================
#普通替换，只替换一个技能id
def replace_one_id(value):
    #return pd.to_numeric(value) * 100 + 1
    return get_effect_id(value)

#VectorSequence类型字段替换，解析的所有技能id都替换
def replace_all(value):
    lists = unpack_to_lists(value)
    for i in range(len(lists)):
        element = lists[i]
        for j in range(len(element)):
                #element[j] = pd.to_numeric(element[j]) * 100 + 1
                element[j] = get_effect_id(element[j])
    return pack_to_str(lists)

#VectorSequence类型字段替换，包含技能id下标和等级下标的参数
def replace_id_iv(value, args):
    skill_id_index = args[0]
    skill_lv_index = args[1] if len(args)>1 else None
    lv = None

    lists = unpack_to_lists(value)
    for i in range(len(lists)):
        element = lists[i]
        for j in range(len(element)):
            if j == skill_id_index:
                #print("before= ", element[skillIdIndex])
                lv = element[skill_lv_index] if not skill_lv_index == None and len(element) > skill_lv_index else 1
                #element[skill_id_index] = pd.to_numeric(element[skill_id_index])*100 + pd.to_numeric(lv)
                element[skill_id_index] = get_effect_id(element[skill_id_index])
                #print("after= ", element[skillIdIndex])
    return pack_to_str(lists)

#任务字段处理，目标类型|目标参数=参数数量|寻路场景id=X=Y=Z
def replace_task(value):
    lists = unpack_to_lists(value)
    if len(lists) > 1 and (lists[0] == 24 or lists[0] == 26):
        #lists[1] = lists[1] * 100 + 1
        lists[1] = get_effect_id(lists[1])
    return pack_to_str(lists)

#每个字符串与技能id一一匹配，如果匹配到则更改技能id（有风险，更改完需要再次确认下是否替换了应该替换的）
def replace_match_id(value):
    lists = unpack_to_lists(value)
    for i in range(len(lists)):
        element = lists[i]
        for j in range(len(element)):
            try:
                if any((SKILL_ID_COLUNM.str.contains(element[j]))):
                    #element[j] = pd.to_numeric(element[j])*100 + 1
                    element[j] = get_effect_id(element[j])
            except:
                continue
        return pack_to_str(lists)

#类型=技能id=等级类型的字段解析
def replace_card_attribute(value, args):
    _type = args[0]
    lists = unpack_to_lists(value)
    for i in range(len(lists)):
        element = lists[i]
        if element[0] == str(_type):
            skill_id = element[1]
            skill_level = element[2]
            #element[1] = pd.to_numeric(element[1])*100 + pd.to_numeric(skill_level)
            element[1] = get_effect_id(element[1])

    return pack_to_str(lists)

#PresentTable的特殊处理
def replace_present_table(value):
    lists = unpack_to_lists(value)
    if lists[0][0] == '1':
        #lists[1][0] = pd.to_numeric(lists[1][0]) * 100 + 1
        lists[1][0] = get_effect_id(lists[1][0])
        return pack_to_str(lists)
    return value

def to_do(value):
    return value
#============================替换函数 End============================

CSV_CONFIG = [
    ["EntityTable", ["UnitSkillID"], [replace_id_iv], [[0,1]]],
    ["EquipReformSkillTable", ["SkillID"], [replace_one_id]],
    ["SkillComboTable", ["Combo","ReplaceSkillId"], [replace_all, replace_one_id]],
    ["MercenaryTable", ["Skill"], [replace_id_iv], [[0,1]]],
    ["MerchantMakeMaterialsTable", ["Unlock"], [replace_id_iv], [[0,1]]],
    ["ProfessionTable", ["SkillIds","RootTransfromSkills","ParentTransfromSkills","CommonAttackSkillID","FixedSkillIds","FixedUnlockSkillIds","FixedCommonSkillIds"], [replace_all, replace_all, replace_all,replace_all,replace_id_iv], [None, None, None,None,[0,1]]],
    ["SlimeTable", ["Skill","DefaultSkill"], [replace_id_iv], [[0,1]]],
    ["MerchantMakeEnchantTable", ["UnlockSkillID"], [replace_id_iv], [[0,1]]],
    ["CareerPreviewTable", ["RecommendedSkills"], [replace_id_iv], [[0,1]]],
    ["AlchemistMake", ["Unlock"], [replace_id_iv], [[0,1]]],
    ["ScrollMakeTable", ["Unlock"], [replace_id_iv], [[0,1]]],
    ["CartRemouldTable", ["UnlockSkillID"], [replace_id_iv], [[0,1]]],
    ["QTEGuideTable", ["SkillId","ShowSkillId"], [replace_one_id]],
    ["QTESkillTable", ["SkillGroup"], [replace_id_iv], [[0,1]]],
    #----------------------------------task---start-------------------------------------------
    ["TaskTable/TaskTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitWorldTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitWeekTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitTrackTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitPostcardTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitPetTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitMercenaryTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitMedalTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitLifeTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitJobTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitInterestingmeetTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitGuildTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitGuideTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitExploreTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitEvilTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitEntrustTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitEdenTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitDungeonsTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitDailyTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitCupidTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitChallengeTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitBranchTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitAdventureTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/TaskSplitActivityTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TaskTable/AllTaskTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    ["TechCenterTable/AllTaskTable", ["Target1","Target2","Target3","Target4","Target5"], [replace_task]],
    #----------------------------------task---end-------------------------------------------
    ["AutoAddSkilPointDetailTable", ["AddSkillQueue"], [replace_id_iv], [[0,1]]],
    ["FirstComboSkillTable", ["SkillID"], [replace_one_id]],
    ["LeaderMethodSkillTable", ["SkillID"], [replace_one_id]],
    ["LeaderMethodDetailTable", ["SkillIds"], [replace_all]],
    ["MonkQTESkillTable", ["FirstSkillID","SecondSkillID","ThirdSkillID","FourthSkillID","FifthSkillID","SixthSkillID"], [replace_one_id]],
    ["MonkQTECustomSkillTable", ["SkillID","ContinueSkillID"], [replace_one_id, replace_all]],
    ["OpenSkillTable", ["SkillIds"], [replace_all]],
    ["SkillClassRecommandTable", ["SkillIds"], [replace_all]],
    ["SkillDataTable", ["SkillId"], [replace_one_id]],
    ["TechCenterTable/SkillDataTable", ["SkillId"], [replace_one_id]],
    ["SkillMatchTable", ["Skill_Id_0","Skill_Id_1","Skill_Id_2","Skill_Id_3","Skill_Id_4"], [replace_one_id]],
    ["TdUnitTable", ["SummonCosts"], [replace_id_iv], [[3]]],
    ["GlobalTableFight", ["Value"], [replace_match_id]],
    ["GlobalTableSystem", ["Value"], [replace_match_id]],
    ["GuildActivityTable", ["Value"], [replace_match_id]],
    ["EquipCardTable", ["CardAttributes"], [replace_card_attribute], [[4]]],
    ["ProfessionPreviewTable", ["SkillClassPreview"], [replace_all]],
    ["AutoAddSkillPointTable", ["ProDetailId"], [replace_all]],
    ["PresentTable", ["BeHitRule"], [replace_present_table]],
]


def start_process(config_row):
    if len(config_row) < 3:
        print("error! configRow.length < 3") 
        return False
    
    table_name = config_row[0]
    filed_list = config_row[1]
    func_list = config_row[2]
    param_list = None
    if len(config_row)>3:
        param_list = config_row[3]

    columns_index_list = []
    func = None
    columns_index = 0
    value = None
    params = None
    try:
        df = pd.read_csv(os.path.join(CSV_PATH, table_name + ".csv"))#.dropna(axis='columns', how='all')
    except Exception as e:
        print("读取csv出错： "+ str(e))
        return False
    row_count = len(df)
    #收集目标列的索引
    for i in range(len(filed_list)):
        try:
            index = df.columns.get_loc(filed_list[i])
        except:
            print('表：' + table_name + ' 没找不到字段' + filed_list[i])
            return False
        else:
            columns_index_list.append(index)
    
    #列和行的遍历
    for i in range(len(columns_index_list)):
        columns_index = columns_index_list[i]
        if len(func_list)-1 >= i:
            func = func_list[i]
            if not param_list == None:
                params = param_list[i]
        for row_index in range(1,row_count):
            value = df.iloc[row_index, columns_index]
            if not pd.isna(value) and not value == "0" and not value == "" and not value == " ":
                result = func(value, params) if not params == None else func(value)
                df.iloc[row_index, columns_index] = result

    #空列名还原为空
    df = df.rename(columns=lambda x: "" if not x.find("Unnamed:") == -1 else x)
    #导出文件
    try:
        if CREATE_NEW_FILE == True:
            target_file_path = os.path.join(CSV_NEW_PATH, table_name + "_new" +".csv")
            target_folder_path = os.path.dirname(target_file_path)
            if not os.path.exists(target_folder_path):
                os.makedirs(target_folder_path)
        else:
            target_file_path = os.path.join(CSV_PATH, table_name +".csv")
        df.to_csv(target_file_path, index=False, encoding="utf_8_sig")
    except Exception as e:
        print("导出失败：" + target_file_path + "     原因：" + str(e))
        return False
    else:
        print("导出成功：" + target_file_path)


#获取EffectIDs字段的第一个数值
def get_effect_ids_first(str):
    return VectorToTable(str)

#存储老skillId与对应skillEffectId的映射
def find_and_save(value):
    idStr = value["Id"]
    effectIdStr = value["EffectIDs"]
    if pd.isna(effectIdStr) or effectIdStr == '' or effectIdStr == " ":
        effectId = idStr
    else:
        effectId = VectorToTable(effectIdStr)[0]

    SKILL_EFFECT_MAP[idStr] = effectId
    #print("skillId = {0} effectId = {1}".format(idStr, effectId))

#将映射表导出为csv
def output_map_to_csv():
    skill_id_list = SKILL_EFFECT_MAP.keys()
    effect_id_list = SKILL_EFFECT_MAP.values()
    out_dic = {'origion_id':skill_id_list, 'replaced_id':effect_id_list}
    map_df = pd.DataFrame.from_dict(out_dic)
    map_df.to_csv("./技能Id替换映射表.csv", index=False, encoding="utf_8_sig")
    print(map_df)

def main():
    global SKILL_ID_COLUNM
    skill_df = pd.read_csv(os.path.join(CSV_PATH, "SkillTable.csv")).drop([0])
    SKILL_ID_COLUNM = skill_df["Id"]
    skill_df.apply(find_and_save, axis = 1)
    output_map_to_csv()

    for i in range(len(CSV_CONFIG)):
        result = start_process(CSV_CONFIG[i])
        if result == False:
            continue
    os.system("pause")

main()
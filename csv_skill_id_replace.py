from pickle import TRUE
import pandas as pd
import os

CSV_PATH = "./CSV"
CSV_NEW_PATH = "./NewCSV/"
CREATE_NEW_FILE = False
Skill_Ids = None

'''def VectorToTable(value):
    vector = value.split('|')
    return vector'''

def UnpackToLists(value):
    vector = value.split('|')
    for i in range(len(vector)):
        sequence = vector[i].split('=')
        vector[i] = sequence
    return vector

def PackToStr(value):
    Str = ""
    for i in range(len(value)):
        sequence = value[i]
        for j in range(len(sequence)):
            if pd.isna(sequence[j]):
                continue
            Str = Str + str(sequence[j])
            if not j == len(sequence)-1:
                Str = Str + '='
        if not i == len(value)-1:
            Str = Str + '|'

    return Str

#============================替换函数 Start============================
#普通替换，只替换一个技能id
def replace_one_id(value):
    return pd.to_numeric(value) * 100 + 1

#VectorSequence类型字段替换，解析的所有技能id都替换
def replace_all(value):
    lists = UnpackToLists(value)
    for i in range(len(lists)):
        element = lists[i]
        for j in range(len(element)):
                element[j] = pd.to_numeric(element[j]) * 100 + 1
    return PackToStr(lists)

#VectorSequence类型字段替换，包含技能id下标和等级下标的参数
def replace_id_iv(value, args):
    skillIdIndex = args[0]
    skillLvIndex = args[1] if len(args)>1 else None
    lv = None

    lists = UnpackToLists(value)
    for i in range(len(lists)):
        element = lists[i]
        for j in range(len(element)):
            if j == skillIdIndex:
                #print("before= ", element[skillIdIndex])
                lv = element[skillLvIndex] if not skillLvIndex == None and len(element) > skillLvIndex else 1
                element[skillIdIndex] = pd.to_numeric(element[skillIdIndex])*100 + pd.to_numeric(lv)
                #print("after= ", element[skillIdIndex])
    return PackToStr(lists)

#任务字段处理，目标类型|目标参数=参数数量|寻路场景id=X=Y=Z
def replace_task(value):
    lists = UnpackToLists(value)
    if len(lists) > 1 and (lists[0] == 24 or lists[0] == 26):
        lists[1] = lists[1] * 100 + 1
    return PackToStr(lists)

#每个字符串与技能id一一匹配，如果匹配到则更改技能id（有风险，更改完需要再次确认下是否替换了应该替换的）
def replace_match_id(value):
    lists = UnpackToLists(value)
    for i in range(len(lists)):
        element = lists[i]
        for j in range(len(element)):
            try:
                if any((Skill_Ids.str.contains(element[j]))):
                    element[j] = pd.to_numeric(element[j])*100 + 1
            except:
                continue
        return PackToStr(lists)

def Todo(value):
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
    #["EquipTable", ["EntryAttributeOne","EntryAttributeTwo"], [Todo]],
    #["EquipHoleTable", ["Property"], [Todo]],
    #["GlobalTableFight", ["Value"], [replace_match_id]],
    #["GlobalTableSystem", ["Value"], [replace_match_id]],
    #["GuildActivityTable", ["Value"], [replace_match_id]],
]

def StartProcess(configRow):
    if len(configRow) < 3:
        print("error! configRow.length < 3") 
        return False
    
    tableName = configRow[0]
    filedList = configRow[1]
    funcList = configRow[2]
    paramList = None
    if len(configRow)>3:
        paramList = configRow[3]

    columnsIndexList = []
    func = None
    columnsIndex = 0
    value = None
    params = None
    data = pd.read_csv(os.path.join(CSV_PATH, tableName + ".csv"))#.dropna(axis='columns', how='all')
    rowCount = len(data)
    #收集目标列的索引
    for i in range(len(filedList)):
        try:
            index = data.columns.get_loc(filedList[i])
        except:
            print('表：' + tableName + ' 没找不到字段' + filedList[i])
            return False
        else:
            columnsIndexList.append(index)
    
    #列和行的遍历
    for i in range(len(columnsIndexList)):
        columnsIndex = columnsIndexList[i]
        if len(funcList)-1 >= i:
            func = funcList[i]
            if not paramList == None:
                params = paramList[i]
        for rowIndex in range(1,rowCount):
            value = data.iloc[rowIndex, columnsIndex]
            if not pd.isna(value) and not value == "0" and not value == "" and not value == " ":
                result = func(value, params) if not params == None else func(value)
                data.iloc[rowIndex, columnsIndex] = result

    #空列名还原为空
    data = data.rename(columns=lambda x: "" if not x.find("Unnamed:") == -1 else x)
    #导出文件
    try:
        if CREATE_NEW_FILE == True:
            targetFilePath = os.path.join(CSV_NEW_PATH, tableName + "_new" +".csv")
            targetFolderPath = os.path.dirname(targetFilePath)
            if not os.path.exists(targetFolderPath):
                os.makedirs(targetFolderPath)
        else:
            targetFilePath = os.path.join(CSV_PATH, tableName +".csv")
        data.to_csv(targetFilePath, index=False, encoding="utf_8_sig")
    except Exception as e:
        print("导出失败：" + targetFilePath + "     原因：" + str(e))
        return False
    else:
        print("导出成功：" + targetFilePath)

def main():
    global Skill_Ids
    Skill_Ids = pd.read_csv(os.path.join(CSV_PATH, "SkillTable.csv"))["Id"]
    for i in range(len(CSV_CONFIG)):
        result = StartProcess(CSV_CONFIG[i])
        if result == False:
            continue
    os.system("pause")

main()
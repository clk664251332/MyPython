from numpy import True_
import pandas as pd
import os

CSV_PATH = "./CSV"
Test = False
TestFiles = ['./CSV/DungeonStandardAttrTable.csv']
Files = []
ExcludeList = [
    "SkillTable.csv",
    "SkillPetTable.csv",
    "SkillEffectTable.csv",
    "SkillEffectPetTable.csv",
    "SkillEffectUuidTable.csv",
    "AttraddRecomTable.csv",
    "AttraddMatchTable.csv",
    "AwardTable.csv",
    "AwardDataTable.csv",
    "CountTable.csv",
    "ConvenientAccountTable.csv",
    ]

data = pd.read_csv(os.path.join(CSV_PATH, "SkillTable.csv"))
skill_ids = data["Id"]

def UnpackToLists(value):
    vector = str(value).split('|')
    for i in range(len(vector)):
        sequence = vector[i].split('=')
        vector[i] = sequence
    return vector

def OnGetValue(value):
    if pd.isna(value):
        return
    list = UnpackToLists(value)
    for i in list:
        for j in i:
            if not j.isdigit() or pd.isna(j) or j == "0":
                continue
            if int(j) < 5000:
                continue
            try:
                if(any(skill_ids.str.contains(j, regex = False))):
                    return True
            except Exception as e:
                #print("执行contains异常： "+"value= "+j+str(e))
                return False
    return False

def main():
    f = open("columnCount.txt","w")
    if not Test:
        for root, dirs, files in os.walk(CSV_PATH, topdown = True):
            for name in files:
                if name not in ExcludeList and name.endswith(".csv"):
                    Files.append(os.path.join(root, name))
    else:
        for test in TestFiles:
            Files.append(test)
    #遍历每一个文件
    for file_path in Files:
        columns = []
        print('*'*15+"处理 " + file_path+'*'*15)
        f.writelines('*'*20 + file_path + '*'*20+'\n')
        df = pd.read_csv(file_path)
        df = df.drop(df.columns[0], axis = 1)
        try:    
            for column in df:
                for value in df[column]:
                    ret = OnGetValue(value)
                    if ret:
                        if not column in columns:
                            columns.append(column)
                        #f.writelines('column = '+column+"  value = "+value+'\n')
            for column in columns:
                f.writelines('column = '+column+'   【'+ df[column][0]+'】\n')
        except Exception as e:
            print("处理"+file_path+"出现问题："+str(e))
            continue

    f.close()

    os.system("pause")
main()
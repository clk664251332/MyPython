import pandas as pd
import os

CSV_PATH = "./CSV"

#Files = ['./CSV/SkillComboTable.csv']
Files = []
ExcludeList = [
    "SkillTable.csv",
    "SkillPetTable.csv",
    "SkillEffectTable.csv",
    "SkillEffectPetTable.csv",
    "SkillEffectUuidTable.csv",
    ]

data = pd.read_csv(os.path.join(CSV_PATH, "SkillTable.csv"))
skill_ids = data["Id"]
#print(any(skill_ids.str.contains('5009')))

def UnpackToLists(value):
    vector = value.split('|')
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
            if pd.isna(j):
                continue
            if(any(skill_ids.str.contains(j))):
                return True
    return False

def main():
    f = open("count.txt","w")
    for root, dirs, files in os.walk(CSV_PATH, topdown = True):
        for name in files:
            if name not in ExcludeList and name.endswith(".csv"):
                Files.append(os.path.join(root, name))
    try:
        for file_path in Files:
            print("处理 " + file_path)
            f.writelines('*'*20 + file_path + '*'*20)
            df = pd.read_csv(file_path)
            for column in df:
                for value in df[column]:
                    ret = OnGetValue(value)
                    if ret:
                        f.writelines('column = '+column+"  value = "+value)
    except Exception as e:
        print("报错： "+ str(e))
        f.close()
    else:
        f.close()

    os.system("pause")
main()
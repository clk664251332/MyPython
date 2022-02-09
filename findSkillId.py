import pandas as pd
import os

CSV_PATH = "./CSV"

Files = ['./CSV/SkillComboTable.csv']
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
    print(value.name)
    list = UnpackToLists(value)
    for i in list:
        for j in i:
            if pd.isna(j):
                continue
            if(any(skill_ids.str.contains(j))):
                print("包含")

def main():
    for root, dirs, files in os.walk(CSV_PATH, topdown = True):
        for name in files:
            if name not in ExcludeList and name.endswith(".csv"):
                Files.append(os.path.join(root, name))

        for file_path in Files:
            df = pd.read_csv(file_path)
            df.applymap(OnGetValue)

def Test():
    for file_path in Files:
        df = pd.read_csv(file_path)
        df.applymap(OnGetValue) 

Test()
from cmath import nan
import pandas as pd
import os
import re

#读取目标文件，获取文件名字
#截取文件名字，获得电影名
#从csv中读取对应的演员名字
#拼接新的文件名字，并重命名

file_path = r"K:\vr\欧美\StasyQVR\new"
csv_path = r".\StasyQvr演员表.csv"
reg_pattern = r"(.*?)_"

df = pd.read_csv(csv_path)
movie_list = df.loc[:,"Movie"].values.tolist()
actor_list = df.loc[:,"Actor"].values.tolist()

file_full_name_list = os.listdir(file_path) #获取文件夹下所有的文件
for file_full_name in file_full_name_list:
    movie_name = re.findall(reg_pattern, file_full_name)[0]
    if movie_name in movie_list:
        index = movie_list.index(movie_name)
        actor_name = actor_list[index]
        if pd.isna(actor_name):
            continue
        new_file_full_name = '('+ actor_name +')'+ file_full_name
        os.rename(os.path.join(file_path, file_full_name), os.path.join(file_path, new_file_full_name))
        print(new_file_full_name)

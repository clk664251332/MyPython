import os,shutil

files = []
delete_dirs = []
suffixs = ("3gp","avi","flv","mkv","mov","mp4","mpeg","mpg","rm","rmvb","ts","vob","webm","wmv")

def travel(path):
    result_list = []
    file_list = os.listdir(path) #获取文件夹下所有的文件
    for cur_file in file_list: #循环遍历每一个文件
        temp_path = os.path.join(path, cur_file) #获取该文件的绝对路径
        if os.path.isdir(temp_path): #如果是文件夹
            travel(temp_path) #递归
            continue
        if os.path.isfile(temp_path): #如果是文件
            if temp_path.lower().endswith(suffixs): #判断文件后缀
                result_list.append(temp_path) #添加到结果列表
    if len(result_list) == 1:  #判断该文件夹是否只有一个视频文件
        files.append(result_list[0])
        delete_dirs.append(path)

#提取出文件夹下所有单独的视频文件
cur_dir_path = os.getcwd()
travel(cur_dir_path)
for file in files:
    shutil.move(file, cur_dir_path)
    print("移出文件: " + file)
for delete_dir in delete_dirs:
    os.rmdir(delete_dir)
    print("删除文件夹: " + delete_dir)

os.system("pause")
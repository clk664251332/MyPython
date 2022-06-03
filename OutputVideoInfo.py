#该脚本用于输出文件夹下所有视频的信息

from asyncio.windows_events import NULL
from pydoc import doc
from xml.etree.ElementTree import tostring
from pymediainfo import MediaInfo
import pandas as pd
import os

DIR_PATH = "D:\\Video"

all_file_name = []
all_file_size = []
all_code_format = []
all_bit_rate = []
all_resolution = []


def ExtractInfo(path):
    media_info = MediaInfo.parse(path)
    data = media_info.to_data()
    info_list = data['tracks']
    general_info = info_list[0]
    video_info = info_list[1]
    audio_info = info_list[2]

    file_name = general_info['file_name_extension']
    file_size = general_info['other_file_size'][0]
    code_format = general_info['codecs_video']
    bit_rate = video_info['other_bit_rate'][0]
    resolution_width = video_info['width']
    resolution_height = video_info['height']
    resolution = str(resolution_width) + " x " + str(resolution_height)

    # print("file_name = " + file_name )
    # print("file_size = " + file_size)
    # print("code_format = " + code_format)
    # print("bit_rate = " + bit_rate)
    # print("resolution = " + resolution)

    all_file_name.append(file_name)
    all_file_size.append(file_size)
    all_code_format.append(code_format)
    all_bit_rate.append(bit_rate)
    all_resolution.append(resolution)




#遍历文件夹下所有的视频文件
AllFilesPath = []    
for root, dirs, files in os.walk(DIR_PATH):
    for name in files:
        if name.endswith(".mp4"):
            AllFilesPath.append(os.path.join(root, name))

for file in AllFilesPath:
    ExtractInfo(file)

data = {
    'file_name':all_file_name, #文件名
    'file_size':all_file_size,#文件大小
    'code_format':all_code_format,#编码格式
    'bit_rate':all_bit_rate,#码率
    'resolution':all_resolution,#分辨率
}
df = pd.DataFrame(data)
df.to_csv('视频格式统计表.csv', index=False, encoding='utf-8')
os.system("pause")
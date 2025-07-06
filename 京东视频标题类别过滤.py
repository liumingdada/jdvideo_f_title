import os
import shutil
import PySimpleGUI as sg
import json
import subprocess

# 指定文件夹路径和关键词列表
folder_path = "D:\\京东采集融合视频\\2024-09-28_467819200-467820000-待上传-5\\1600"
folder_path = r"D:\京东采集融合视频\2024-09-28_467819200-467820000-待上传-5\NFACE"
keywords = ['服装', '鞋','靴', '衣服', '裤', '裙', '衫', '帽子', '外套', '夹克', '箱包', '饰品', '首饰', '穿搭', '时尚','显瘦', '女装', '男装', '文胸', '胸罩']
keywords11 = ["美食", "好吃", "美味", "咸菜", "生鲜", "调料", "酒", "饮料", "养生", "茶", "糖", "醋", "豆油", "食品", "海鲜", "鱼", "营养", "零食","品尝"]

def DoSearchByKW(keywords,folder_path):
    # 创建新文件夹
    new_folder_name = keywords[0]
    new_folder_path = os.path.join(folder_path, new_folder_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    # 遍历指定文件夹下的所有.mp4文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith((".mp4", ".mp5")):
            file_path = os.path.join(folder_path, file_name)
            for keyword in keywords:
                if keyword in file_name:
                    shutil.move(file_path, os.path.join(new_folder_path, file_name))
                    break
    print("已完成...")            



# 从JSON文件中读取数据
with open('jdTitleCatKW.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 提取类别和关键词信息
categories = [category["name"] for category in data["categories"]]
keywords_dict = {category["name"]: category["keywords"] for category in data["categories"]}

# 创建PySimpleGUI界面
layout = [
    [sg.Text("选择类别："), sg.Combo(categories, key="category", enable_events=True),
     sg.Button('编辑类别',font=("微软雅黑", 10),button_color ='Green'),
     ],
    [sg.FolderBrowse("视频目录", target="folder_path"), sg.InputText(key="folder_path",size=30)],
    [  sg.Output(size=(40, 10), key="output")],
    [ sg.Button('开始过滤',font=("微软雅黑", 10),button_color ='Blue'),],
]

window = sg.Window("类别关键词选择器", layout)

# 事件循环
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    selected_category = values["category"]
    if selected_category:
        keywords = keywords_dict.get(selected_category, [])
        print(keywords)

    if event == '编辑类别':    
        print("编辑类别") 
        subprocess.Popen(['notepad.exe', 'jdTitleCatKW.json']) 

    if event == '开始过滤':  
        folder_path = values["folder_path"] 
        keywords = keywords_dict.get(selected_category, [])  
        DoSearchByKW(keywords,folder_path)

window.close()

# pyinstaller -F -w -i iconJDpro.ico 京东视频标题类别过滤.py 
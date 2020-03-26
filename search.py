import os
import requests
from module import get_image

def Search(api_key,api_secret):
    """
    在一个已有的 FaceSet 中找出与目标人脸最相似的一张或多张人脸
    :param api_key:
    :param api_secret:
    :return:
    """
    url = "https://api-cn.faceplusplus.com/facepp/v3/search"
    data = {"api_key": api_key, "api_secret": api_secret}
    while True:
        type = input("""
                \n请选择搜寻模式（输入数字）：
                1.利用图片进行搜寻
                2.利用 face_token 进行比对
                3.退出
                """)
        aim = input("请输入目标人脸的 face_token ：")
        if aim != None and type!=None and aim.strip()!="" and type.strip()!="":
            if "1" in type:
                file =""
                while file==None or file.strip()=="":
                    file = input("请输入被搜寻图片的磁盘路径(支持相对路径)：")
                data["image_base64"] = get_image(file)
            elif "2" in type:
                token = ""
                while token == None or token.strip() == "":
                    token = input("请输入被搜寻图片的 face_token：")
                data["faceset_token"] = token
            elif "3" in type:
                break
            else:
                print("输入错误！")
                continue
            result = requests.post(url, data).json()
        else:
            print("输入错误！")
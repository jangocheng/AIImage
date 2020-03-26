# -*- coding:utf-8 -*-
#developer:倪小白
#blog:www.nixiaobai.com
#Face++ https://www.faceplusplus.com.cn
import os

from detect import Detect
from compare import Compare
from search import Search
from beautify import Beautify
from facialfeatures import FacialFeatures
from skinanalyze import SkinAnalyze
from face_3d import Face_3d
from gesture import Gesture
from merge import Merge

#用户key&secret
api_key = "lRxJfI3QovHo9SPsZMQamnJZoIfR9YP8"
api_secret = "RFV35OzPrS2Sam-XcPx52m89jqjD5lY5"

if __name__ == "__main__":
    # 在脚本根目录新建缓存文件夹
    if not os.path.exists("log"):
        os.mkdir("log")
    if not os.path.exists("cache"):
        os.mkdir("cache")

    print("欢迎使用倪小白的 AI图片识别脚本 当前版本4.0")
    print("开发者博客：https://www.nixiaobai.com")
    print("本脚本调用旷视 Face++ API，使用请遵循 Face++ 的相关协议，本软件仅供个人学习研究所用，禁止用于商业用途！")
    print("请尽量将图片放在本执行文件目录，避免报错！")
    print("网络api请求受限，请不要频繁使用本软件。禁止用于非法用途！")

    dict ={
        1:Detect,
        2:Compare,
        3:Search,
        4:Beautify,
        5:FacialFeatures,
        6:SkinAnalyze,
        7:Face_3d,
        8:Gesture,
        9:Merge
    }

    while True:
        key = input("""
        #################################
        主菜单：(请输入对应功能数字并按Enter键)
        【建议使用相对路径图片，避免错误】
        1.人脸检测
        2.人脸比对
        3.人脸搜寻[无法使用]
        4.AI美颜
        5.面部分析
        6.皮肤分析
        7.3D人脸模型
        8.手势识别
        9.AI换脸
        0.退出软件
        """)
        try:
            type = int(key)
            if type == 0:
                break
            else:
                dict.get(type)(api_key,api_secret)
        except Exception as e:
            print("错误：{}".format(e))

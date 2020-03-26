import os
import requests
from module import get_image, Base64ToObj,logTime

def Face_3d(api_key,api_secret):
    """
    可根据单张或多张单人人脸图片，重建3D人脸效果。
    :param api_key:
    :param api_secret:
    :return:
    """
    url = "https://api-cn.faceplusplus.com/facepp/v1/3dface"
    data = {"api_key": api_key, "api_secret": api_secret,"texture":1,"mtl":1}

    if not os.path.exists("3d"):
        os.mkdir("3d")

    value =1
    while True:
        type = input("你想使用几张人脸图片合成3D模型？【1~3】：")
        try:
            value = int(type)
            break
        except:
            print("输入错误")
    if value>3: value = 3
    for i in range(value):
        v = i + 1
        img = input("请输入图片 {} 磁盘路径(支持相对路径)：".format(v))
        data["image_base64_{}".format(v)] = get_image(img)

    result = requests.post(url, data).json()
    if result != None and "error_message" not in result:
        request_id = result["request_id"]
        time_used = result["time_used"]
        print("请求ID：{}".format(request_id))
        print("请求耗时：{}毫秒".format(time_used))

        obj_file = result["obj_file"]
        Base64ToObj(obj_file,"3d/face.obj")
        texture_img = result["texture_img"]
        Base64ToObj(texture_img, "3d/tex.jpg")
        mtl_file = result["mtl_file"]
        Base64ToObj(mtl_file, "3d/face.mtl")
        print("3d文件夹下已生成 face.obj【模型】，face.mtl【材质】，tex.jpg【纹理】 文件")
        print("请用C4D、3Dmax、Maya等建模工具打开 obj 文件")
        transfer_matrix = result["transfer_matrix"]
        print("3D模型视角变换矩阵：")
        print(transfer_matrix)
        input("按下Enter键回到主菜单")
        return result
    else:
        print("网络请求错误")
        return

import os
import requests
from module import get_image, logTime


def Compare(api_key,api_secret):
    """
    将两个人脸进行比对，来判断是否为同一个人，返回比对结果置信度和不同误识率下的阈值。
    支持传入图片或 face_token 进行比对。使用图片时会自动选取图片中检测到人脸尺寸最大的一个人脸。
    :param api_key:
    :param api_secret:
    :return: json[result],confidence
    """
    url = "https://api-cn.faceplusplus.com/facepp/v3/compare"
    data = {"api_key": api_key, "api_secret": api_secret}
    while True:
        type = input("""
        \n请选择对比模式（输入数字）：
        1.利用图片进行比对
        2.利用 face_token 进行比对
        3.退出
        """)

        if type !=None and "1" in type:
            img1 = input("请输入图片 1 磁盘路径(支持相对路径)：")
            img2 = input("请输入图片 2 磁盘路径(支持相对路径)：")
            if img1 and img1.strip() != "" and  img2 and img2.strip() != "" and os.path.exists(img1) and os.path.exists(img2):
                data["image_base64_1"] = get_image(img1)
                data["image_base64_2"] = get_image(img2)
            else:
                print("图片路径有错误！")
        elif type !=None and "2" in type:
            img1 = input("请输入图片 1 的 face_token：")
            img2 = input("请输入图片 2 的 face_token：")
            if img1 and img1.strip() != "" and  img2 and img2.strip() != "":
                data["face_token1"] = img1.strip()
                data["face_token2"] = img2.strip()
            else:
                print("图片 face_token 有错误！")
        elif type != None and "3" in type:
            break
        else:
            print("输入错误！")
            continue

        result = requests.post(url, data).json()
        if result !=None and "error_message" not in result:
            #用于区分每一次请求的唯一的字符串。
            request_id = result["request_id"]
            #比对结果置信度，范围 [0,100]，小数点后3位有效数字，数字越大表示两个人脸越可能是同一个人。
            confidence = result["confidence"]
            #一组用于参考的置信度阈值，包含以下三个字段。每个字段的值为一个 [0,100] 的浮点数，小数点后 3 位有效数字。
            thresholds = result["thresholds"]
            #1e-3：误识率为千分之一的置信度阈值；
            value_1e_3 = thresholds["1e-3"]
            #1e-4：误识率为万分之一的置信度阈值；
            value_1e_4 = thresholds["1e-4"]
            #1e-5：误识率为十万分之一的置信度阈值；
            value_1e_5 = thresholds["1e-5"]
            if float(confidence) > float(value_1e_5):
                confidence_rank = "十万分之一的误识率"
            elif float(confidence) > float(value_1e_4):
                confidence_rank = "万分之一的误识率"
            else:confidence_rank = "千分之一的误识率"

            #图片在系统中的标识
            if "image_id1" in result and "image_id2" in result:
                image_id1 = result["image_id1"]
                image_id2 = result["image_id2"]
            else:
                image_id1 = "无"
                image_id2 = "无"
            #检测出的人脸数组，采用数组中的第一个人脸(最凸显的人脸)进行人脸比对
            if "faces1" in result and "faces2" in result:
                faces1 = result["faces1"]
                faces2 = result["faces2"]
            else:
                faces1 = "1"
                faces2 = "1"
            #整个请求所花费的时间
            time_used = result["time_used"]

            txt = """
            \n本次网络请求用时： {time_used} 毫秒 
            请求ID ： {request_id}
            图片 1 ID ： {image_id1}
            图片 1 共检测出 {faces1} 张人脸（默认采用最凸显的人脸）
            图片 2 ID ： {image_id2}
            图片 2 共检测出 {faces2} 张人脸（默认采用最凸显的人脸）
            
            【{confidence_rank}】
            2 张人脸拥有 {confidence}% 相似度
            """.format(time_used=time_used,request_id=request_id,image_id1=image_id1,image_id2=image_id2,
                       faces1=len(faces1),faces2=len(faces2),confidence_rank=confidence_rank,confidence=confidence)
            print(txt)
            f = open("log/{}.txt".format(logTime()), "w")
            f.write(txt)
            f.close()
            input("按下Enter键回到主菜单")
            return result,confidence
        else:
            print("网络请求错误！")



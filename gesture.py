import os
import requests
from module import get_image, Base64ToObj,logTime

def Gesture(api_key,api_secret):
    """
    检测图片中出现的所有的手部，并返回其在图片中的矩形框位置与相应的手势含义。目前可以识别 19 种手势。
    :param api_key:
    :param api_secret:
    :return:
    """
    url = "https://api-cn.faceplusplus.com/humanbodypp/v1/gesture"
    data = {"api_key": api_key, "api_secret": api_secret}
    img = input("请输入手势图片磁盘路径(支持相对路径)：")
    if img and img.strip() != "" and os.path.exists(img):
        data["image_base64"] = get_image(img)
        result = requests.post(url, data).json()
        if result != None and "error_message" not in result:
            time_used = result["time_used"]  # 整个请求所花费的时间，单位为毫秒。
            image_id = result["image_id"]  # 被检测的图片在系统中的标识。
            request_id = result["request_id"]  # 用于区分每一次请求的唯一的字符串。

            hands = result["hands"]
            hand_value = len(hands)

            print("""\n本次网络请求用时：{time_used}毫秒 
            请求ID：{request_id}
            检测图片路径为：{img}
            检测图片ID：{image_id}
            共检测出 {hand_value} 个手势""".format(time_used=time_used,request_id=request_id,img=img,image_id=image_id,hand_value=hand_value))

            dict = {
                "unknown": "未知",
                "heart_a": "比心 A：手背朝画面，心尖向下，拇指指尖接触",
                "heart_b": "比心 B：手指第二关节接触，心尖向下，拇指指尖接触",
                "heart_c": "比心 C：手腕接触，心尖向下，剩下四指左右两手接触",
                "heart_d": "比心 D：食指大拇指交叉，食指朝上，其余手指折叠",
                "ok": "OK：食指拇指尖接触，剩余手指摊开",
                "hand_open": "手张开：五指打开，手心面向画面",
                "thumb_up": "点赞：竖大拇指，方向向上",
                "thumb_down": "差评：竖大拇指，方向向下",
                "rock": "ROCK：小拇指、食指、大拇指伸直，无名指、中指折起，手心对外",
                "namaste": "合十：双手合十",
                "palm_up": "手心向上：摊开手，手心朝上",
                "fist": "握拳：握拳，手心对外",
                "index_finger_up": "食指朝上：伸出食指，其余手指折起，手心对外",
                "double_finger_up": "双指朝上：伸出食指和中止，并拢，其余手指折起，手心对外",
                "victory": "胜利	：伸出食指和中止，张开，其余手指折起，手心对外",
                "big_v": "大V：伸出食指和大拇指，其余手指折起，手背朝外",
                "phonecall": "打电话：伸出大拇指和小指，其余手指折叠，手背对外",
                "beg": "作揖：一手握拳，另一手覆盖在其之上",
                "thanks": "感谢：一手握拳，另一手张开，手心覆盖在其之上"
            }

            count = 0
            for item in hands:
                count+=1
                width = item["hand_rectangle"]["width"]
                top = item["hand_rectangle"]["top"]
                height = item["hand_rectangle"]["height"]
                left = item["hand_rectangle"]["left"]
                print("\n手势{count}：".format(count=count))
                ges = item["gesture"]
                ges_max = max(ges, key=lambda k: ges[k])
                print(dict.get(ges_max,"未知"))
                print("""宽度：{width} 像素    高度：{height} 像素    左上角横坐标：{left}    左上角纵坐标：{top}""".format(count=count,width=width,height=height,left=left,top=top))
            input("\n按下Enter键回到主菜单")
            return result
        else:
            print("网络错误！")
    else:
        print("输入错误！")
        return
import os
import requests
from module import get_image, logTime


def Detect(api_key,api_secret):
    """
    检测图片中的人脸（支持一至多张人脸），并标记出边框。您也可以对尺寸最大的5张人脸进行分析，获得面部关键点、年龄、性别、头部姿态、微笑检测、眼镜检测以及人脸质量等信息。
    :param api_key:
    :param api_secret:
    :return: json,[face_token]
    """

    img = input("请输入图片磁盘路径(支持相对路径):")
    if img and img.strip() != "" and os.path.exists(img):
        image_base64 = get_image(img)
        url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
        data = {"api_key": api_key,
                "api_secret": api_secret,
                "image_base64": image_base64,
                "return_attributes": "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus",
                "beauty_score_min": 0,
                "beauty_score_max": 100}
        result = requests.post(url, data).json()
        if result != None and "error_message" not in result:
            time_used = result["time_used"]  # 整个请求所花费的时间，单位为毫秒。
            face_num = result["face_num"]  # 检测出的人脸个数
            image_id = result["image_id"]  # 被检测的图片在系统中的标识。
            request_id = result["request_id"]  # 用于区分每一次请求的唯一的字符串。

            print("""
            \n本次网络请求用时：{time_used}毫秒 
            请求ID：{request_id}
            检测图片路径为：{img}
            检测图片Base64:{image_base64}
            检测图片ID：{image_id}
            共检测出 {face_num} 张人脸
            """.format(time_used=time_used, img=img, image_id=image_id, request_id=request_id, face_num=face_num,
                       image_base64=image_base64))
            face_id = []
            for index in range(0, len(result["faces"])):
                # 人脸反馈内容
                it = result["faces"][index]
                # 人脸的标识
                face_token = it["face_token"]
                face_id.append(face_token)
                # 人脸矩形框的位置
                face_rectangle = it["face_rectangle"]
                width = face_rectangle["width"]  # 矩形框的宽度
                height = face_rectangle["height"]  # 矩形框的高度
                face_left = face_rectangle["left"]  # 矩形框左上角像素点的横坐标
                face_top = face_rectangle["top"]  # 矩形框左上角像素点的纵坐标
                # 人脸属性内容
                attr = result["faces"][index]["attributes"]
                # 性别分析结果
                if attr["gender"]["value"] == "Male":
                    gender = "男性"
                elif attr["gender"]["value"] == "Female":
                    gender = "女性"

                # 年龄分析结果
                age = attr["age"]["value"]

                # 笑容分析结果
                smile_value = attr["smile"]["value"]
                if int(float(smile_value)) > 50:
                    smile = "【有】 程度{}%".format(smile_value)
                else:
                    smile = "【无】 程度{}%".format(smile_value)

                # 人脸姿势分析结果
                headpose = attr["headpose"]
                # 抬头角度
                pitch_angle = headpose["pitch_angle"]
                # 旋转（平面旋转）角度
                roll_angle = headpose["roll_angle"]
                # 摇头角度
                yaw_angle = headpose["yaw_angle"]

                # 人脸模糊分析结果
                blur = attr["blur"]
                # 人脸移动模糊度分析结果
                motionblur = blur["motionblur"]["value"]
                # 人脸高斯模糊度分析结果
                gaussianblur = blur["gaussianblur"]["value"]
                # 新型人脸模糊分析结果
                blurness = blur["blurness"]["value"]

                # 眼睛状态信息
                eyestatus = attr["eyestatus"]
                left_eye_status = eyestatus["left_eye_status"]
                right_eye_status = eyestatus["right_eye_status"]
                left_eye_max = max(left_eye_status, key=lambda k: left_eye_status[k])
                right_eye_max = max(right_eye_status, key=lambda k: right_eye_status[k])
                eye = {
                    "occlusion": "眼睛被遮挡",
                    "no_glass_eye_open": "不戴眼镜且睁眼",
                    "normal_glass_eye_close": "佩戴普通眼镜且闭眼",
                    "normal_glass_eye_open": "佩戴普通眼镜且睁眼",
                    "dark_glasses": "佩戴墨镜",
                    "no_glass_eye_close": "不戴眼镜且闭眼"
                }
                left_eye = eye.get(left_eye_max, "不戴眼镜且睁眼")  # 文字表示
                left_eye_value = left_eye_status[left_eye_max]  # 置信度
                right_eye = eye.get(right_eye_max, "不戴眼镜且睁眼")
                right_eye_value = right_eye_status[right_eye_max]

                # 情绪识别结果
                emotion = attr["emotion"]
                anger = emotion["anger"]  # 愤怒
                disgust = emotion["disgust"]  # 厌恶
                fear = emotion["fear"]  # 恐惧
                happiness = emotion["happiness"]  # 高兴
                neutral = emotion["neutral"]  # 平静
                sadness = emotion["sadness"]  # 伤心
                surprise = emotion["surprise"]  # 惊讶

                # 人脸照片质量
                facequality = attr["facequality"]["value"]

                # 人种分析结果
                ethnicity = attr["ethnicity"]["value"]
                if str(ethnicity).strip() == "": ethnicity = "未知"

                # 颜值识别结果
                beauty = attr["beauty"]
                male_score = beauty["male_score"]  # 男性认为的此人脸颜值分数
                female_score = beauty["female_score"]  # 女性认为的此人脸颜值分数

                # 嘴部状态信息
                mouthstatus = attr["mouthstatus"]
                mouth_max = max(mouthstatus, key=lambda k: mouthstatus[k])
                mouth = {"surgical_mask_or_respirator": "嘴部被医用口罩或呼吸面罩遮挡",
                         "other_occlusion": "嘴部被其他物体遮挡",
                         "close": "嘴部没有遮挡且闭上",
                         "open": "嘴部没有遮挡且张开"}.get(mouth_max, "嘴部没有遮挡且闭上")
                mouth_value = mouthstatus[mouth_max]

                # 眼球位置与视线方向信息
                eyegaze = attr["eyegaze"]
                left_eye_gaze = eyegaze["left_eye_gaze"]
                right_eye_gaze = eyegaze["right_eye_gaze"]

                # 面部特征识别结果
                skinstatus = attr["skinstatus"]
                health = skinstatus["health"]  # 健康
                stain = skinstatus["stain"]  # 色斑
                acne = skinstatus["acne"]  # 青春痘
                dark_circle = skinstatus["dark_circle"]  # 黑眼圈

                txt = """
                \n人脸{index} 检测结果如下:
                人脸标识：{face_token}
                照片质量：{facequality} 分
                人脸模糊度：{blur}%
                人脸矩形框：
                宽度：{width} 像素    高度：{height} 像素
                左上角横坐标：{face_left}    左上角纵坐标：{face_top}
    
                性别：{gender}  年龄：{age} 岁
                人种分析:{ethnicity}
                人脸姿势：抬头 {pitch_angle}°  转头 {roll_angle}°  摇头 {yaw_angle}°
                笑容：{smile}
                眼睛状态: 
                【左眼】{left_eye} 置信度 {left_eye_value}%
                【右眼】{right_eye} 置信度 {right_eye_value}%
                嘴部状态：{mouth} 置信度 {mouth_value}%
                情绪识别:
                {anger}% 愤怒   {disgust}% 厌恶   {fear}% 恐惧
                {happiness}% 高兴   {neutral}% 平静   {sadness}% 伤心   {surprise}% 惊讶
                颜值识别：男性评分：{male_score}分   女性评分：{female_score}分
                面部特征：健康 {health}%   色斑 {stain}%   青春痘 {acne}%   黑眼圈 {dark_circle}%
                """.format(
                    index=index + 1, facequality=facequality,
                    blur=int((float(blurness) + float(gaussianblur) + float(motionblur)) / 3),
                    gender=gender, age=age, ethnicity=ethnicity, pitch_angle=pitch_angle, roll_angle=roll_angle,
                    yaw_angle=yaw_angle,
                    smile=smile, left_eye=left_eye, left_eye_value=left_eye_value, right_eye=right_eye,
                    right_eye_value=right_eye_value,
                    mouth=mouth, mouth_value=mouth_value, anger=anger, disgust=disgust, fear=fear, happiness=happiness,
                    neutral=neutral,face_token =face_token,
                    sadness=sadness, surprise=surprise, male_score=float(male_score), female_score=float(female_score), health=health,
                    stain=stain, acne=acne, dark_circle=dark_circle,width=width,height=height,face_left=face_left,face_top=face_top)

                f = open("log/{}.txt".format(logTime()), "w")
                f.write(txt)
                f.close()

                print(txt)
            for index in range(0,len(face_id)):
                print("人脸{index} face_token ： {id}".format(index=index + 1,id=face_id[index]))
            input("按下Enter键回到主菜单")
            return result,face_id
        else:
            print("网络请求错误！")
    else:
        print("图片路径错误或不存在")


import os
import requests
from module import get_image, Base64ToObj,logTime

def SkinAnalyze(api_key,api_secret):
    """
    对人脸图片，进行面部皮肤状态检测分析
    :param api_key:
    :param api_secret:
    :return:
    """
    url = "https://api-cn.faceplusplus.com/facepp/v1/skinanalyze_advanced"
    data = {"api_key": api_key, "api_secret": api_secret}
    while True:
        img = input("请输入需要检测面容的图片磁盘路径(支持相对路径):")
        if img != None and img.strip()!="" and os.path.exists(img):
            data["image_base64"] = get_image(img)
            result = requests.post(url, data).json()

            if result != None and "error_message" not in result:
                # 请求ID
                request_id = result["request_id"]
                # 人脸矩形框的位置
                top = result["face_rectangle"]["top"]
                left = result["face_rectangle"]["left"]
                width = result["face_rectangle"]["width"]
                height = result["face_rectangle"]["height"]
                # 整个请求所花费的时间，单位为毫秒
                time_used = result["time_used"]

                it=result["result"]
                #肤色
                skin_color = {"0":"透白","1":"白皙","2":"自然","3":"小麦","4":"黝黑"}.get(str(it["skin_color"]["value"]), "未知")
                skin_color_c = it["skin_color"]["confidence"]

                #肤龄
                skin_age = it["skin_age"]["value"]

                #右眼双眼皮检测
                right_eyelids = {"0": "单眼皮", "1": "平行双眼皮", "2": "扇形双眼皮"}.get(str(it["right_eyelids"]["value"]), "未知")
                right_eyelids_c = it["right_eyelids"]["confidence"]

                #左眼双眼皮检测
                left_eyelids = {"0":"单眼皮","1":"平行双眼皮","2":"扇形双眼皮"}.get(str(it["left_eyelids"]["value"]),"未知")
                left_eyelids_c = it["left_eyelids"]["confidence"]

                #眼袋检测
                eye_pouch = {"0":"无眼袋","1":"有眼袋"}.get(str(it["eye_pouch"]["value"]), "未知")
                eye_pouch_c = it["eye_pouch"]["confidence"]

                #黑眼圈检测
                dark_circle = {"0":"无黑眼圈","1":"色素型黑眼圈","2":"血管型黑眼圈","3":"阴影型黑眼圈"}.get(str(it["dark_circle"]["value"]), "未知")
                dark_circle_c = it["dark_circle"]["confidence"]

                #抬头纹检测
                forehead_wrinkle = {"0": "无抬头纹", "1": "有抬头纹"}.get(str(it["forehead_wrinkle"]["value"]), "未知")
                forehead_wrinkle_c = it["forehead_wrinkle"]["confidence"]

                #鱼尾纹检测
                crows_feet = {"0": "无鱼尾纹", "1": "有鱼尾纹"}.get(str(it["crows_feet"]["value"]), "未知")
                crows_feet_c = it["crows_feet"]["confidence"]

                #眼部细纹检测
                eye_finelines = {"0": "无眼部细纹", "1": "有眼部细纹"}.get(str(it["eye_finelines"]["value"]), "未知")
                eye_finelines_c = it["eye_finelines"]["confidence"]

                #眉间纹检测
                glabella_wrinkle = {"0": "无眉间纹", "1": "有眉间纹"}.get(str(it["glabella_wrinkle"]["value"]), "未知")
                glabella_wrinkle_c = it["glabella_wrinkle"]["confidence"]

                #法令纹检测
                nasolabial_fold = {"0": "无法令纹", "1": "有法令纹"}.get(str(it["nasolabial_fold"]["value"]), "未知")
                nasolabial_fold_c = it["nasolabial_fold"]["confidence"]

                #肤质检测
                types = it["skin_type"]["details"]
                type = 0
                value = 0
                for k in types:
                    i = types[k]
                    if float(i["confidence"]) > type:
                        type = float(i["confidence"])
                        value = i["value"]
                skin_type = {"0":"油性皮肤","1":"干性皮肤","2":"中性皮肤","3":"混合性皮肤"}.get(str(value), "未知")
                skin_type_c = type

                #前额毛孔检测
                pores_forehead = {"0": "前额无毛孔粗大", "1": "前额有毛孔粗大"}.get(str(it["pores_forehead"]["value"]), "未知")
                pores_forehead_c = it["pores_forehead"]["confidence"]

                #左脸颊毛孔检测
                pores_left_cheek = {"0": "左脸颊无毛孔粗大", "1": "左脸颊有毛孔粗大"}.get(str(it["pores_left_cheek"]["value"]), "未知")
                pores_left_cheek_c = it["pores_left_cheek"]["confidence"]

                #右脸颊毛孔检测
                pores_right_cheek = {"0": "右脸颊无毛孔粗大", "1": "右脸颊有毛孔粗大"}.get(str(it["pores_right_cheek"]["value"]), "未知")
                pores_right_cheek_c = it["pores_right_cheek"]["confidence"]

                #下巴毛孔检测结果
                pores_jaw = {"0": "下巴无毛孔粗大", "1": "下巴有毛孔粗大"}.get(str(it["pores_jaw"]["value"]), "未知")
                pores_jaw_c = it["pores_jaw"]["confidence"]

                #黑头检测结果
                blackhead = {"0": "无黑头", "1": "轻度", "2": "中度","3":"重度"}.get(str(it["blackhead"]["value"]), "未知")
                blackhead_c = it["blackhead"]["confidence"]

                #痘痘检测结果
                acne = len(it["acne"]["rectangle"])

                #痣检测结果
                mole = len(it["mole"]["rectangle"])

                # 斑点检测结果
                skin_spot = len(it["skin_spot"]["rectangle"])

                txt="""
                本次请求用时：{time_used} 毫秒
                人脸矩形框：
                宽度：{width} 像素    高度：{height} 像素
                左上角横坐标：{left}    左上角纵坐标：{top}
                
                肤色{skin_color}    置信度：{skin_color_c}%
                肤龄：{skin_age} 岁

                右眼{right_eyelids}   置信度：{right_eyelids_c}%
                左眼{left_eyelids}   置信度：{left_eyelids_c}%
                眼袋{eye_pouch}   置信度：{eye_pouch_c}%
                {dark_circle}   置信度：{dark_circle_c}%
 
                {skin_type}   置信度：{skin_type_c}%
                {forehead_wrinkle}   置信度：{forehead_wrinkle_c}%
                {crows_feet}   置信度：{crows_feet_c}%
                {eye_finelines}   置信度：{eye_finelines_c}%
                {glabella_wrinkle}   置信度：{glabella_wrinkle_c}%
                {nasolabial_fold}   置信度：{nasolabial_fold_c}%
                {pores_forehead}   置信度：{pores_forehead_c}%
                {pores_left_cheek}   置信度：{pores_left_cheek_c}%
                {pores_right_cheek}   置信度：{pores_right_cheek_c}%
                
                {pores_jaw}   置信度：{pores_jaw_c}%
                黑头检测：{blackhead}    置信度：{blackhead_c}%
                痘痘检测：{acne}
                痣检测：{mole}
                斑点检测：{skin_spot} 
                """.format(nasolabial_fold=nasolabial_fold,time_used=time_used,width=width,height=height,left=left,top=top,skin_color=skin_color,skin_color_c=skin_color_c,skin_age=skin_age,right_eyelids=right_eyelids,right_eyelids_c=right_eyelids_c,left_eyelids=left_eyelids,left_eyelids_c=left_eyelids_c,eye_pouch=eye_pouch,eye_pouch_c=eye_pouch_c,dark_circle=dark_circle,dark_circle_c=dark_circle_c,forehead_wrinkle=forehead_wrinkle,forehead_wrinkle_c=forehead_wrinkle_c,crows_feet=crows_feet,crows_feet_c=crows_feet_c,eye_finelines=eye_finelines,eye_finelines_c=eye_finelines_c,glabella_wrinkle=glabella_wrinkle,glabella_wrinkle_c=glabella_wrinkle_c,nasolabial_fold_c=nasolabial_fold_c,skin_type=skin_type,skin_type_c=skin_type_c,pores_forehead=pores_forehead,pores_forehead_c=pores_forehead_c,pores_left_cheek=pores_left_cheek,pores_left_cheek_c=pores_left_cheek_c,pores_right_cheek=pores_right_cheek,pores_right_cheek_c=pores_right_cheek_c,pores_jaw=pores_jaw,pores_jaw_c=pores_jaw_c,blackhead=blackhead,blackhead_c=blackhead_c,acne=acne,mole=mole,skin_spot=skin_spot)
                print(txt)
                f = open("log/{}.txt".format(logTime()), "w")
                f.write(txt)
                f.close()
                input("按下Enter键回到主菜单")
                return result

            else:
                print("网络请求错误！")
        else:
            print("输入错误！")
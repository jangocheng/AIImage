import os
import requests
from module import get_image, Base64ToObj


def Beautify(api_key,api_secret):
    """
    支持对图片中人像进行对美颜美型处理，以及对图像增加滤镜等。美颜包括：美白和磨皮；美型包括：大眼、瘦脸、小脸和去眉毛等处理。
    :param api_key:
    :param api_secret:
    :return:
    """
    url = "https://api-cn.faceplusplus.com/facepp/v2/beautify"
    data = {"api_key": api_key, "api_secret": api_secret}
    while True:
        img = input("请输入需要美化的图片磁盘路径(支持相对路径):")
        if img and img.strip() != "" and os.path.exists(img):
            img_base = get_image(img)
            data["image_base64"] = img_base
            print("请输入美颜参数：【默认为50】")

            whitening = input("请输入美白程度0~100：")
            if whitening==None or whitening.strip()=="":
                whitening = 50
            else:
                whitening = int(float(whitening))
            data["whitening"] = whitening

            smoothing = input("请输入磨皮程度0~100：")
            if smoothing == None or smoothing.strip() == "":
                smoothing = 50
            else:
                smoothing = int(float(smoothing))
            data["smoothing"] = smoothing

            thinface = input("请输入瘦脸程度0~100：")
            if thinface == None or thinface.strip() == "":
                thinface = 50
            else:
                thinface = int(float(thinface))
            data["thinface"] = thinface

            shrink_face = input("请输入小脸程度0~100：")
            if shrink_face == None or shrink_face.strip() == "":
                shrink_face = 50
            else:
                shrink_face = int(float(shrink_face))
            data["shrink_face"] = shrink_face

            enlarge_eye = input("请输入大眼程度0~100：")
            if shrink_face == None or enlarge_eye.strip() == "":
                enlarge_eye = 50
            else:
                enlarge_eye = int(float(enlarge_eye))
            data["enlarge_eye"] = enlarge_eye

            remove_eyebrow = input("请输入去眉毛程度0~100：")
            if remove_eyebrow == None or remove_eyebrow.strip() == "":
                remove_eyebrow = 50
            else:
                remove_eyebrow = int(float(remove_eyebrow))
            data["remove_eyebrow"] = remove_eyebrow

            filter_txt="""
                滤镜类型：
                0   无滤镜
                1   black_white	黑白
                2   calm	平静
                3	sunny	晴天
                4	trip	旅程
                5	beautify	美肤
                6	wangjiawei	王家卫
                7	cutie	唯美
                8	macaron	可人儿
                9	new_york	纽约
                10	sakura	樱花
                11	17_years_old	十七岁
                12	clight	柔光灯
                13	tea_time	下午茶
                14	whiten	亮肤
                15	chaplin	卓别林
                16	flowers	花香
                17	memory	回忆
                18	ice_lady 冰美人
                19	paris	巴黎
                20	times	时光
                21	lomo	LOMO
                22	old_times	旧时光
                23	spring	早春
                24	story	故事
                25	abao	阿宝色
                26	wlight	补光灯
                27	warm	暖暖
                28	glitter  绚烂
                29	lavender	薰衣草
                30	chanel	香奈儿
                31	prague	布拉格
                32	old_dream	旧梦
                33	blossom	桃花
                34	pink	粉黛
                35	jiang_nan	江南
                请输入滤镜类型数字：
                """
            f_type = ""
            f_type = input(filter_txt)
            type_list={
                "1":"black_white",
                "2":"calm",
                "3":"sunny",
                "4":"trip",
                "5":"beautify",
                "6":"wangjiawei",
                "7":"cutie",
                "8":"macaron",
                "9":"new_york",
                "10":"sakura",
                "11":"17_years_old",
                "12":"clight",
                "13":"tea_time",
                "14":"whiten",
                "15":"chaplin",
                "16":"flowers",
                "17":"memory",
                "18":"ice_lady" ,
                "19":"paris",
                "20":"times",
                "21":"lomo",
                "22":"old_times",
                "23":"spring",
                "24":"story",
                "25":"abao",
                "26":"wlight",
                "27":"warm",
                "28":"glitter",
                "29":"lavender",
                "30":"chanel",
                "31":"prague",
                "32":"old_dream",
                "33":"blossom",
                '34':"pink",
                '35':"jiang_nan"
            }
            if f_type==None and f_type.strip()=="":
                if int(f_type.strip()) in range(1,36):
                    data["filter_type"] = type_list[f_type.strip()]

            result = requests.post(url, data).json()
            if result != None and "error_message" not in result:
                print("本次请求ID：{}".format(result["request_id"]))
                print("本次请求用时 {} 毫秒".format(result["time_used"]))
                Base64ToObj(result["result"],'ai_{}'.format(img))
                print("成功生成 ai_{} 图片文件".format(img))
                input("按Enter键回到主菜单")
                return result
            else:
                print("网络请求错误！")
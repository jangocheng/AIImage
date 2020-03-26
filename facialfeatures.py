import os
import requests
from module import get_image, Base64ToObj,logTime

def FacialFeatures(api_key,api_secret):
    """
    根据单张正面人脸图片，分析人脸面部特征。
    :param api_key:
    :param api_secret:
    :return:json
    """
    url = "https://api-cn.faceplusplus.com/facepp/v1/facialfeatures"
    data = {"api_key": api_key, "api_secret": api_secret}

    type = input("请输入数字选择类型：\n1->本地图片\n2->网络图片\n")
    if type!=None and type.strip()!="":
        if "2" in type:
            img = input("请输入图片直链网址(记得要加前缀):")
            if img != None and img.strip()!="":
                data["image_url"] = img
            else:
                print("错误")
                return
        else:
            img = input("请输入需要检测面容的图片磁盘路径(支持相对路径):")
            if img != None and img.strip()!="":
                data["image_base64"] = get_image(img)
            else:
                print("错误")
                return

        # 返回人脸矫正结果
        data["return_imagereset"] = 1
        result = requests.post(url, data).json()
        if result != None and "error_message" not in result:
            #请求ID
            request_id = result["request_id"]
            #图片ID
            image_id = result["image_id"]
            #矫正后图片
            image_reset = result["image_reset"]
            Base64ToObj(image_reset,"reset_{}".format(img))
            #人脸矩形框的位置
            top = result["face_rectangle"]["top"]
            left = result["face_rectangle"]["left"]
            width = result["face_rectangle"]["width"]
            height = result["face_rectangle"]["height"]
            #人脸姿势分析结果
            pitch_angle = result["headpose"]["pitch_angle"]
            roll_angle = result["headpose"]["roll_angle"]
            yaw_angle = result["headpose"]["yaw_angle"]
            #整个请求所花费的时间，单位为毫秒
            time_used = result["time_used"]

            #人脸特征分析的结果
            it = result["result"]
            #三庭
            #三庭比例
            three_parts = it["three_parts"]
            parts_ratio = three_parts["parts_ratio"]
            #上庭
            one_part = three_parts["one_part"]
            faceup_value = one_part["faceup_ratio"]
            faceup_result = one_part["faceup_result"]
            faceup = {"faceup_normal":"上庭标准","faceup_long":"上庭偏长","faceup_short":"上庭偏短"}.get(faceup_result)
            #中庭
            two_part = three_parts["two_part"]
            facemid_value = two_part["facemid_ratio"]
            facemid_result = two_part["facemid_result"]
            facemid = {"facemid_normal":"中庭标准","facemid_long":"中庭偏长","facemid_short":"中庭偏短"}.get(facemid_result)
            #下庭
            three_part = three_parts["three_part"]
            facedown_value = three_part["facedown_ratio"]
            facedown_result = three_part["facedown_result"]
            facedown = {"facedown_normal":"下庭标准","facedown_long":"下庭偏长","facedown_short":"下庭偏短"}.get(facedown_result)

            #五眼
            five_eyes = it["five_eyes"]
            #五眼比例
            eyes_ratio = five_eyes["eyes_ratio"]
            #眼部宽度
            righteye = five_eyes["righteye"]
            lefteye = five_eyes["lefteye"]
            #五眼右侧分析结果
            righteye_empty_result = five_eyes["one_eye"]["righteye_empty_result"]
            one_eye = {"righteye_empty_normal":"右眼外侧适中","righteye_empty_short":"右眼外侧偏窄","righteye_empty_long":"右眼外侧偏宽"}.get(righteye_empty_result)
            #内眼角间距分析结果
            eyein_result = five_eyes["three_eye"]["eyein_result"]
            three_eye = {"eyein_normal":"内眼角间距适中","eyein_short":"内眼角间距偏窄","eyein_long":"内眼角间距偏宽"}.get(eyein_result)
            #五眼左侧分析结果
            lefteye_empty_result = five_eyes["five_eye"]["lefteye_empty_result"]
            five_eye = {"lefteye_empty_normal":"左眼外侧适中","lefteye_empty_short":"左外外侧偏窄","lefteye_empty_long":"左眼外侧偏宽"}.get(lefteye_empty_result)

            #黄金三角
            golden_triangle = it["golden_triangle"]

            #脸型分析结果
            face = it["face"]
            #颞部宽度
            tempus_length = face["tempus_length"]
            #颧骨宽度
            zygoma_length = face["zygoma_length"]
            #脸部长度
            face_length = face["face_length"]
            #下颌角宽度
            mandible_length = face["mandible_length"]
            #下颌角度数
            E = face["E"]
            #颞部宽度、颧部宽度（固定颧部为1）、下颌角宽度比（若为0则返回null）
            ABD_ratio = face["ABD_ratio"]
            #脸型判断结果
            face_type = {"pointed_face":"瓜子脸","oval_face":"椭圆脸","diamond_face":"菱形脸","round_face":'圆形脸',"long_face":"长形脸","square_face":"方形脸","normal_face":'标准脸'
            }.get(face["face_type"],"未知")

            #下巴分析结果
            jaw = it["jaw"]
            jaw_width = jaw["jaw_width"]
            jaw_length = jaw["jaw_length"]
            jaw_angle = jaw["jaw_angle"]
            jaw_type ={"flat_jaw":"圆下巴","sharp_jaw":"尖下巴","square_jaw":"方下巴"}.get(jaw["jaw_type"],"未知")

            #眉毛分析结果
            eyebrow = it["eyebrow"]
            brow_width = eyebrow["brow_width"]
            brow_height = eyebrow["brow_height"]
            brow_uptrend_angle = eyebrow["brow_uptrend_angle"]
            brow_camber_angle = eyebrow["brow_camber_angle"]
            brow_thick = eyebrow["brow_thick"]
            eyebrow_type = {"bushy_eyebrows":"粗眉","eight_eyebrows":"八字眉","raise_eyebrows":'上挑眉',"straight_eyebrows":"一字眉","round_eyebrows":"拱形眉","arch_eyebrows":"柳叶眉","thin_eyebrows":"细眉"
            }.get(eyebrow["eyebrow_type"],"未知")

            #眼睛分析结果
            eyes = it["eyes"]
            eye_width = eyes["eye_width"]
            eye_height = eyes["eye_height"]
            angulus_oculi_medialis = eyes["angulus_oculi_medialis"]
            eyes_type = {"round_eyes":"圆眼","thin_eyes":"细长眼","big_eyes":'大眼',"small_eyes":"小眼",'normal_eyes':'标准眼'
                         }.get(eyes["eyes_type"],"未知")

            #鼻子分析结果
            nose = it["nose"]
            nose_width = nose["nose_width"]
            nose_type = {"normal_nose":"标准鼻","thick_nose":"宽鼻","thin_nose":'窄鼻'
                         }.get(nose["nose_type"],"未知")

            #嘴唇分析结果
            mouth = it["mouth"]
            mouth_height = mouth["mouth_height"]
            mouth_width = mouth["mouth_width"]
            lip_thickness = mouth["lip_thickness"]
            angulus_oris = mouth["angulus_oris"]
            mouth_type = {"thin_lip":"薄唇","thick_lip":"厚唇","smile_lip":"微笑唇","upset_lip":'态度唇','normal_lip':'标准唇'
            }.get(mouth["mouth_type"],"未知")

            txt="""
            本次请求用时：{time_used} 毫秒
            图片ID:{image_id}
            矫正图片 ai_{img} 已生成！
            人脸姿势分析：抬头 {pitch_angle}°  转头 {roll_angle}°  摇头 {yaw_angle}°
            人脸矩形框：
                宽度：{width} 像素    高度：{height} 像素
                左上角横坐标：{left}    左上角纵坐标：{top}
            
            人脸特征分析的结果：
            三庭比例:{parts_ratio}
            上庭比例:{faceup_value}%   {faceup}  
            中庭比例:{facemid_value}%   {facemid}
            下庭比例:{facedown_value}%   {facedown}
            
            五眼比例:{eyes_ratio}
            {one_eye}  {three_eye}  {five_eye}
            右眼宽度：{righteye}mm     左眼宽度：{lefteye}mm
            
            眼型：{eyes_type}
            宽度：{eye_width}mm    高度：{eye_height}mm
            内眦角度数：{angulus_oculi_medialis}°
            
            黄金三角度数：{golden_triangle}°
            
            脸型：{face_type}
            颞部宽度：{tempus_length}mm
            颧骨宽度：{zygoma_length}mm
            脸部长度：{face_length}mm
            下颌角宽度：{mandible_length}mm
            下颌角度数：{E}°
            颞部宽度、颧部宽度（固定颧部为1）、下颌角宽度比：{ABD_ratio}
            
            下巴：{jaw_type}
            宽度：{jaw_width}mm   长度：{jaw_length}mm   角度：{jaw_angle}°
            
            眉毛：{eyebrow_type}  粗细：{brow_thick}mm
            宽度：{brow_width}mm    高度：{brow_height}mm
            挑度：{brow_uptrend_angle}°    弯度：{brow_camber_angle}°
            
            鼻型：{nose_type}    鼻翼宽度：{nose_width}mm
            
            唇型判断：{mouth_type}
            高度：{mouth_height}mm    宽度：{mouth_width}mm
            厚度：{lip_thickness}mm    嘴角弯曲度：{angulus_oris}°
            """.format(
                time_used=time_used,image_id=image_id,img=img,
                pitch_angle=pitch_angle,roll_angle=roll_angle,yaw_angle=yaw_angle,
                width=width,height=height,left=left,top=top,
                parts_ratio=parts_ratio,faceup_value=faceup_value,faceup=faceup,
                facemid_value=facemid_value,facemid=facemid,facedown_value=facedown_value,facedown=facedown,
                eyes_ratio=eyes_ratio, one_eye=one_eye, three_eye=three_eye, five_eye=five_eye, righteye=righteye,
                lefteye=lefteye, eyes_type=eyes_type, eye_width=eye_width, eye_height=eye_height,
                angulus_oculi_medialis=angulus_oculi_medialis, golden_triangle=golden_triangle, face_type=face_type,
                tempus_length=tempus_length, zygoma_length=zygoma_length, face_length=face_length,
                mandible_length=mandible_length, E=E, ABD_ratio=ABD_ratio, jaw_type=jaw_type, jaw_width=jaw_width,
                jaw_length=jaw_length, jaw_angle=jaw_angle, eyebrow_type=eyebrow_type, brow_thick=brow_thick,
                brow_width=brow_width, brow_height=brow_height, brow_uptrend_angle=brow_uptrend_angle,
                brow_camber_angle=brow_camber_angle, nose_type=nose_type, nose_width=nose_width, mouth_type=mouth_type,
                mouth_height=mouth_height, mouth_width=mouth_width, lip_thickness=lip_thickness,
                angulus_oris=angulus_oris
            )

            print(txt)
            f = open("log/{}.txt".format(logTime()),"w")
            f.write(txt)
            f.close()
            input("按下Enter键回到主菜单")
            return result
        else:
            print("网络请求错误！")
            return
    else:
        print("错误")
        return
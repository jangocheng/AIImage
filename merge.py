import os
import requests
from module import get_image, Base64ToObj,logTime

def Merge(api_key,api_secret):
    """

    :param api_key:
    :param api_secret:
    :return:
    """
    if not os.path.exists("merge"):
        os.mkdir("merge")
    url = "https://api-cn.faceplusplus.com/imagepp/v1/mergeface"
    data = {"api_key": api_key, "api_secret": api_secret}
    img1 = input("请输入 脸部图片 磁盘路径(支持相对路径)：")
    img2 = input("请输入 模板图片 磁盘路径(支持相对路径)：")
    if img1 and img1.strip() != "" and img2 and img2.strip() != "" and os.path.exists(img1) and os.path.exists(img2):

        data["merge_base64"] = get_image(img1)
        data["template_base64"] = get_image(img2)

        result = requests.post(url, data).json()
        if result != None and "error_message" not in result:
            time_used = result["time_used"]  # 整个请求所花费的时间，单位为毫秒。
            request_id = result["request_id"]  # 用于区分每一次请求的唯一的字符串。
            print("网络耗时：{}毫秒".format(time_used))
            print("请求ID：{}".format(request_id))
            imgdata = result["result"]
            Base64ToObj(imgdata,"merge/merge_{}".format(img1))
            print("成功生成 merge/merge_{} 图片".format(img1))

            input("\n按下Enter键回到主菜单")
            return result
        else:
            print("网络错误！")
    else:
        print("输入错误！")

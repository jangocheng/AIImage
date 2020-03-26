import base64

#字节码读取图片，并且转换成base64编码
import os
from PIL import Image
import time

def logTime():
    # 获得当前时间时间戳
    now = int(time.time())
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", timeArray)
    return otherStyleTime

def Base64ToObj(base,name):
    imgdata = base64.b64decode(base)
    file = open(name, 'wb')
    file.write(imgdata)
    file.close()

def ImgToBase64(file):
    #图片转base64
    with open(file, "rb") as f:
        return str(base64.b64encode(f.read())).replace("b'","").replace("'","")

def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return size / 1024

def compress_image(infile, outfile='', mb=200, step=10, quality=80):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    o_size = get_size(infile)
    if o_size <= mb:
        return infile
    outfile = "mini_{}".format(infile)
    while o_size > mb:
        im = Image.open(infile)
        im.save(outfile, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(outfile)
    return outfile

def resize_image(infile, outfile='', x_s=1000):
    """修改图片尺寸
    :param infile: 图片源文件
    :param outfile: 重设尺寸文件保存地址
    :param x_s: 设置的宽度
    :return:
    """
    im = Image.open(infile)
    x, y = im.size
    y_s = int(y * x_s / x)
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    outfile = "resize_{}".format(infile)
    out.save(outfile)

def get_image(infile):
    resize_image(infile)
    outfile = compress_image("resize_{}".format(infile))
    return ImgToBase64(outfile)
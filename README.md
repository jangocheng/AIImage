# AIImage简介
基于旷视 Face++ (https://www.faceplusplus.com.cn) 封装的python脚本。
纯python，注释清晰，语法简洁

# 开发者
倪小白（ni00）
博客：https://www.nixiaobai.com
Email：mail@nixiaobai.com

# 使用指南
请将main.py中api_key、api_secret填写完整,运行 main.py 即可使用
![截图2](http://image.nixiaobai.com/aiimage/2.png)
![截图1](http://image.nixiaobai.com/aiimage/1.jpg)
# 项目列表如下：
detect.py
> 获得面部关键点、年龄、性别、头部姿态、微笑检测、眼镜检测以及人脸质量等信息

compare.py
> 将两个人脸进行比对，来判断是否为同一个人，返回比对结果置信度和不同误识率下的阈值。

search.py
> 在一个图片中找出与目标人脸最相似的一张或多张人脸

beautify.py
> 对图片中人像进行对美颜美型处理，以及对图像增加滤镜等。美颜包括：美白和磨皮；美型包括：大眼、瘦脸、小脸和去眉毛等处理。

facialfeatures.py
> 根据单张正面人脸图片，分析人脸面部特征。

skinanalyze.py
> 对人脸图片，进行面部皮肤状态检测分析

face_3d.py
> 可根据单张或多张单人人脸图片，重建3D人脸效果。

gesture.py
> 检测图片中出现的所有的手部，并返回其在图片中的矩形框位置与相应的手势含义。目前可以识别 19 种手势。

merge.py
> 可以对模板图和融合图中的人脸进行融合操作。融合后的图片中将包含融合图中的人脸特征，以及模板图中的其他外貌特征与内容。

# TODO
+ 支持所有磁盘路径
+ 支持网络图片
+ 更改压缩算法
+ 更多功能

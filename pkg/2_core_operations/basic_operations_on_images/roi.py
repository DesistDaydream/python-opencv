#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2

# if __name__ == "__main__":
# Region Of Interest(感兴趣的区域，简称 ROI) 就是我们从图像中选择一个图像区域，这个区域是图像分析所关注的焦点。
# 我们圈定这个区域，那么我们要处理的图像就从大图像变为一个小图像区域了，这样以便进行进一步处理，可以大大减小处理时间。

# 读取图片
img = cv2.imread("images/messi5.jpg")

print(img.shape)

# 获取图像中的我们感兴趣的区域，i.e.ROI
# 这里选定的是 “280 行至 340 行” 且 “330 列 至 390 列” 之间所有像素组成的图像
ball = img[280:340, 330:390]

# 将 ROI 覆盖到原图像中的 “273 行至 333 行” 且 “100 列至 160 列” 之间的所有像素
# 其实就是将图片中 273-333 行，100-160 列包围的每一个像素替换为 ball 中的像素
img[273:333, 100:160] = ball

# 效果如下，图像左边会多出一个小球
cv2.imwrite("images/messi5_new.jpg", img)

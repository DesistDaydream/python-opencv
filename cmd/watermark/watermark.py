#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2

# 读入原图
# img1 = cv2.imread("./images/dtcg/original.jpg")
# img2 = cv2.imread("./images/dtcg/watermarked.jpg")
# img1 = cv2.imread("./images/dtcg/cn.png")
# img2 = cv2.imread("./images/dtcg/en.png")

# # 截取 265:337, 32:398 这个位置的图像
# roi1 = img1[265:337, 32:398]
# roi2 = img2[265:337, 32:398]

# # 计算图像差
# diff = cv2.absdiff(roi1, roi2)

# # 保存图像差
# cv2.imwrite("./images/dtcg/watermark.png", diff)

# 加载图片
img = cv2.imread("./images/dtcg/cn.png")
watermark = cv2.imread("./images/dtcg/watermark.png")

# 图片与水印图进行减法运算
result = cv2.subtract(img, watermark)

# 保存结果图
cv2.imwrite("./images/dtcg/result.png", result)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2

# if __name__ == "__main__":
# Region Of Interest(感兴趣的区域，简称 ROI) 就是我们从图像中选择一个图像区域，这个区域是图像分析所关注的焦点。
# 我们圈定这个区域，那么我们要处理的图像就从大图像变为一个小图像区域了，这样以便进行进一步处理，可以大大减小处理时间。
img = cv2.imread("images/roi.jpg")

print(img.shape)

# 获取图像中的我们感兴趣的区域，i.e.ROI
# 这里选定的是 “280 行至 350 行” 且 “330 列 至 390 列” 之间所有像素组成的图像
ball = img[240:280, 280:320]

# 将 ROI 覆盖到原图像中的 “40 行至 80 行” 且 “140 列至 180 列” 之间的所有像素
img[40:80, 140:180] = ball

# cv2.imwrite("images/roi_new.jpg", ball)

cv2.imshow("Window Title", img)
# waitKey() 等待用户按键，若按键为 ESC，则返回 -1。如果不等待，那么打开的窗口瞬间就会关闭
k = cv2.waitKey(0)

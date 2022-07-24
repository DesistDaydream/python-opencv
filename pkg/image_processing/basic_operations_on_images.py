#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2

# 核心操作-图像的基本操作：https://docs.opencv.org/4.x/d3/df2/tutorial_py_basic_ops.html

# 访问和修改图像中像素的值
def AccessingAndModifyingPixelValues(img: cv2.Mat):
    # 通过行和列坐标访问一个像素的值。对于 RGB 图像，返回一个包含蓝色、绿色、红色值得数组。对于灰度图像，只返回相应的强度
    px = img[100, 100]
    print(px)

    # 修改像素的值。
    # 将 100-200 行中第 100-200 列的所有像素的值设为 BGR(0, 0, 255)，即.红色
    # 特别注注意！！！这里的 RGB 不是按照红、绿、蓝的顺序，而是按照 BGR 的顺序
    # 此时打开图像，我们可以看到在 100-200 行中第 100-200 列的所有像素的值都变成了红色，也就是有一个小正方体大小的红色正方体
    img[100:200, 100:200] = [0, 0, 255]
    print(img[100, 100])

    blue = img[100, 100, 0]
    print(blue)

    cv2.imshow("窗口的标题", img)
    # waitKey() 等待用户按键，若按键为 ESC，则返回 -1。如果不等待，那么打开的窗口瞬间就会关闭
    k = cv2.waitKey(0)


# 访问图像的属性
def AccessingImageProperties(img: cv2.Mat):
    # 图像的属性包括行、列、通道数、图像数据的类型、像素数
    # 通过 Mat 的 shape 属性获取图像的行、列、通道数
    print(img.shape)
    # 通过 Mat 的 size 属性获取图像的像素总数
    print(img.size)
    # 通过 Mat 的 dtype 属性获取图像的数据类型
    print(img.dtype)
    # 注意：img.dtype 在调试时非常重要，因为 OpenCV-Python 代码中的大量错误是由无效数据类型引起的


if __name__ == "__main__":
    img = cv2.imread("images/OpenCV_logo.png")
    AccessingAndModifyingPixelValues(img)
    # AccessingImageProperties(img)

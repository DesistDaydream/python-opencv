#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2

# 核心操作-图像的基本操作：https://docs.opencv.org/4.x/d3/df2/tutorial_py_basic_ops.html

# 访问和修改图像中像素的值
def AccessingAndModifyingPixelValues(img: cv2.Mat):
    # 通过行和列坐标访问一个像素的值。
    # - 对于 BGR 图像，返回一个数组，0号元素表示蓝色的值、1号元素表示绿色的值、2号元素表示红色的值。
    # - 对于灰度图像，只返回相应的强度
    # 这里将会返回图像中，第 230 行，第 150 列这个像素的值。
    px = img[230, 150]
    print(px)

    # 修改像素的值。
    # ！！！特别注注意！！！这里的 [0, 0, 255] 不是按照 RGB(i.e.红、绿、蓝)的顺序，而是按照 BGR(i.e.蓝、绿、红) 的顺序
    # 所以这里是将图片中 “从上往下数第 50 行，从左往右数第 60 列” 这个像素的值设为 BGR(0, 0, 255)，即.红色
    img[50, 60] = [0, 0, 255]
    # 注意：Mat 对象实际上是 NumPy 库中的 numpy.ndarray 对象，因此我们可以使用 numpy 的函数来操作它
    # Numpy 通常用来快速数组计算，因此简单得访问每个像素值并对其进行修改将非常难缓慢，并不鼓励这样做

    # 此时打开图像，可以看到图片左上角区域中的一个像素变为了红色
    cv2.imshow("Window Title", img)
    cv2.waitKey(0)

    # 获取图像中，第1行，第1列像素的蓝色通道的值
    # 第三个元素的值:
    # - 0 表示蓝色
    # - 1 表示绿色
    # - 2 表示红色
    # 分别对应 B、G、R 通道
    blue = img[1, 1, 0]
    print(blue)


# 访问和修改图像中像素的值的更好的方法
def BetterAccessingAndModifyingPixelValues(img: cv2.Mat):
    # 访问一个像素的值
    print("img 图像中，第 1 行 230 列像素中，蓝色通道的值为: ", img.item(1, 230, 0))
    print("img 图像中，第 1 行 230 列像素中，绿色通道的值为: ", img.item(1, 230, 1))
    print("img 图像中，第 1 行 230 列像素中，红色通道的值为: ", img.item(1, 230, 2))

    # 修改像素的值。
    # 将图像中,第 1 行 230 列像素中，蓝色通道的值设为 255
    img.itemset((1, 230, 0), 255)

    # 此时打开图像，放大一下,可以看到第 1 行 230 列像素不是红色了，变成了 255,0,255 的颜色，类似粉色
    cv2.imshow("Window Title", img)
    cv2.waitKey(0)


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
    img = cv2.imread("images/OpenCV_logo.png", flags=1)
    AccessingAndModifyingPixelValues(img)
    # BetterAccessingAndModifyingPixelValues(img)
    # AccessingImageProperties(img)

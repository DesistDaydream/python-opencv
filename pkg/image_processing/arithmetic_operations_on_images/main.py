#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2 as cv
import os

# 核心操作-图像的算数运算：https://docs.opencv.org/4.x/d0/d86/tutorial_py_image_arithmetics.html

# 图像混合
def ImageBlending():
    img1 = cv.imread("images/ml.png")
    img2 = cv.imread("images/opencv-logo.png")

    print(img1.shape, img2.shape)

    # 注意：混合两张图片的前提需要保证两张图片的尺寸一致
    dst = cv.addWeighted(img1, 0.7, img2[0:380, 0:308], 0.3, 0)
    cv.imshow("dst", dst)
    cv.waitKey(0)
    cv.destroyAllWindows()


# 按位操作
def BitwiseOperations():
    img = cv.imread("images/messi5.jpg")
    logo = cv.imread("images/opencv-logo-white.png")
    rows, cols, channels = logo.shape
    # 从 img 中取出与 logo 大小相同的 ROI 区域，该区域用来与 logo 合并
    roi = img[0:rows, 0:cols]

    ########
    # 若我们将 logo 直接与 img 合并，则会使得 img 中的 ROI 全部被覆盖，其中还包括 logo 中的后背景。
    # 这种做法是错误的，我们需要先扣除 logo 的后背景
    # img[0:rows, 0:cols] = logo
    ########

    ################################
    # 创建 logo 图像的蒙版和反向蒙版 #
    ################################
    # cv.cvtColor() 函数可以将图像的 BGR 颜色空间转换为另一种颜色空间。https://docs.opencv.org/4.x/d8/d01/group__imgproc__color__conversions.html#ga397ae87e1288a81d2363b61574eb8cab
    # 这里的 COLOR_BGR2GRAY 表示将图像从 BGR 颜色空间转换为 GRAY(灰度) 颜色空间
    img2gray = cv.cvtColor(logo, cv.COLOR_BGR2GRAY)
    # cv.shteshold() 函数可以将图像二值化，即将图像的每个像素的值转换为 0 或 255 。https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html#gae8a4a146d1ca78c626a53577199e9c57
    ret, mask = cv.threshold(img2gray, 10, 255, cv.THRESH_BINARY)
    # cv.bitwise_not() 函数可以对图像进行按位取反操作。https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga0002cf8b418479f4cb49a75442baee2f
    mask_inv = cv.bitwise_not(mask)

    # Now black-out the area of logo in ROI
    img_bg = cv.bitwise_and(roi, roi, mask=mask_inv)
    # 从 logo 图像中取出除了背景以外的像素
    logo_fg = cv.bitwise_and(logo, logo, mask=mask)
    # 将 logo 放入 ROI 并修改 img 图像
    dst = cv.add(img_bg, logo_fg)
    img[0:rows, 0:cols] = dst

    cv.imshow("res", img)
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == "__main__":
    # ImageBlending()
    BitwiseOperations()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import cv2

# OpenCV 中的 GUI 之 图像入门：https://docs.opencv.org/4.x/db/deb/tutorial_display_image.html
def GUIGettingStartedWithImages():
    # imread() 读取图片，并将图片实例化为一个 Mat 对象
    # 可以接收参数以指定我们想要的图像格式
    # - IMREAD_COLOR 以 BGR 8 位格式加载图像。这是此处使用的默认值。
    # - IMREAD_UNCHANGED 按原样加载图像（包括 alpha 通道，如果存在）。其实就是将图片变为黑白的了
    # - IMREAD_GRAYSCALE 将图像作为强度加载
    # image = cv2.imread("images/OpenCV_logo.png")
    image = cv2.imread(cv2.samples.findFile("images/OpenCV_logo.png"), cv2.IMREAD_COLOR)
    # 注意：Mat 对象实际上是 NumPy 库中的 numpy.ndarray 对象，因此我们可以使用 numpy 的函数来操作它

    if image is None:
        sys.exit("无法读取图片")

    # imshow() 打开一个窗口，并显示图片
    cv2.imshow("窗口的标题", image)
    # waitKey() 等待用户按键，若按键为 ESC，则返回 -1。如果不等待，那么打开的窗口瞬间就会关闭
    k = cv2.waitKey(0)

    # ord() 用于等待键盘输入，0 表示任意键。这里按下 s 则会将图片保存到本地
    if k == ord("s"):
        # imwrite() 将 Mat 对象写入图片并保存
        cv2.imwrite("images/OpenCV_logo_save.png", image)


if __name__ == "__main__":
    GUIGettingStartedWithImages()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2

# 循环输出所有色彩空间
for i in dir(cv2):
    if i.startswith("COLOR_"):
        print(i)

# 对于 BGR→灰度转换，我们使用标志 cv.COLOR_BGR2GRAY。同样对于 BGR→HSV，我们使用标志 cv.COLOR_BGR2HSV。

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2

# 教程-图像处理-模板匹配
# https://docs.opencv.org/4.x/de/da9/tutorial_template_matching.html

# 物体检测是一种通过模板匹配技术实现的功能。模板匹配是一种用于查找与模板图像（补丁）匹配（相似）的图像区域的技术。

source_img = "./images/tmpl_matching/source.jpg"
tmpl_img = "./images/tmpl_matching/tmpl.jpg"


i_img = cv2.imread(source_img, 0)
t_img = cv2.imread(tmpl_img, 0)

cv2.imshow("source image", i_img)
cv2.imshow("templateimage", t_img)

th, tw = t_img.shape[:2]  # 获取模板图像的高宽。用来在后面画出匹配到的图像区域

# 测试多种匹配算法的匹配效果
methods = [
    cv2.TM_SQDIFF_NORMED,
    cv2.TM_CCORR_NORMED,
    cv2.TM_CCOEFF_NORMED,
]  # 各种匹配算法
for md in methods:
    mdName = ""
    if md == cv2.TM_SQDIFF_NORMED:
        mdName = "TM_SQDIFF_NORMED"
    elif md == cv2.TM_CCORR_NORMED:
        mdName = "TM_CCORR_NORMED"
    elif md == cv2.TM_CCOEFF_NORMED:
        mdName = "TM_CCOEFF_NORMED"

    matchedResult = cv2.matchTemplate(i_img, t_img, md)
    # result是我们各种算法下匹配后的图像
    cv2.imshow("%s" % md, matchedResult)
    # 获取的是每种公式中计算出来的值，每个像素点都对应一个值
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matchedResult)
    print(mdName, " 的匹配结果: ", min_val, max_val, min_loc, max_loc)

    # 确定匹配区域的左上角和右下角的左边，以便在原图中用矩形框圈出来。
    if md == cv2.TM_SQDIFF_NORMED:
        tl = min_loc  # tl是左上角点
    else:
        tl = max_loc
    br = (tl[0] + tw, tl[1] + th)  # 右下点

    # 画矩形
    cv2.rectangle(i_img, tl, br, (0, 0, 255), 2)
    cv2.imshow("%s-match-%s" % (md, mdName), i_img)

if cv2.waitKey(0) == ord("q"):
    cv2.destroyAllWindows()

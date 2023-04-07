import numpy as np
import cv2

# 创建一张黑色的图片
img = np.zeros((512, 512, 3), np.uint8)

# 绘制一条粗细为 5 px 的蓝色对角线。
cv2.line(img, (0, 0), (511, 511), (255, 0, 0), 5)

# 向图片中添加文本
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, "OpenCV", (10, 500), font, 4, (255, 255, 255), 2, cv2.LINE_AA)

cv2.imwrite("images/drawing.jpg", img)

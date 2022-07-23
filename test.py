import sys
import cv2

if __name__ == "__main__":
    highStart = int(265)  # 高度起点
    highEnd = int(331)  # 高度终点
    wideStart = int(32)  # 宽度起点
    wideEnd = int(398)  # 宽度终点

    SrcFile = "./images_cn/BT1-085R.png"
    DstFile = "./images_new/BT1-085R.png"

    img = cv2.imread(SrcFile)

    cropImg = img[highStart:highEnd, wideStart:wideEnd]

    cv2.imwrite(DstFile, cropImg)

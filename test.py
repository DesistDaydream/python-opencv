import sys
import cv2

if __name__ == "__main__":
    # highStart = int(265)  # 高度起点
    # highEnd = int(350)  # 高度终点(数码宝贝)
    # wideStart = int(32)  # 宽度起点
    # wideEnd = int(398)  # 宽度终点

    highStart = int(265)  # 高度起点
    highEnd = int(330)  # 高度终点(驯兽师、选项)
    wideStart = int(32)  # 宽度起点
    wideEnd = int(398)  # 宽度终点

    CNFile = "BTC2_BT5-092P_D.png"
    ENFile = "BT5-092_P1.png"
    DstFile = "BTC2_BT5-092P_D.png-new.png"

    imageCN = cv2.imread(CNFile)
    imageEN = cv2.imread(ENFile)

    imageCN[highStart:highEnd, wideStart:wideEnd] = imageEN[
        highStart:highEnd, wideStart:wideEnd
    ]

    cv2.imwrite(DstFile, imageCN)

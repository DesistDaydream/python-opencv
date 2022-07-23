import os
import cv2

if __name__ == "__main__":
    highStart = int(265)  # 高度起点
    highEnd = int(350)  # 高度终点
    wideStart = int(32)  # 宽度起点
    wideEnd = int(398)  # 宽度终点

    # 从 images_en 中读取 BT1- 开头的图像
    # filepathEN = "./images_en"  # 需要裁剪源图像
    # filepathCN = "./images_cn"  # 将裁剪的图像合并到这个目录下的图片
    filepathEN = "/mnt/e/Projects/DesistDaydream/dtcg/images/en/BT01-03"  # 需要裁剪源图像
    filepathCN = (
        "/mnt/e/Projects/DesistDaydream/dtcg/images/cn/BTC-01"  # 将裁剪的图像合并到这个目录下的图片
    )
    destpath = "/mnt/e/Projects/DesistDaydream/dtcg/images/cn-prefect/BT-01"  # resized images saved here

    # 逐一处理 filepathCN 中的图片
    filesCN = os.listdir(filepathCN)
    for fileCN in filesCN:
        # 如果图片的名称以 BT1- 开头，并且第八个字符为字母，则处理该图片
        if fileCN.startswith("BT1-") and fileCN[7].isalpha():
            # 读取 BT1- 开头的图像
            imageCN = cv2.imread(os.path.join(filepathCN, fileCN))
            # 取出 BT1- 后面的数字
            numCN = fileCN[4:7]

            # 如果 nmuCN 小于 084
            if int(numCN) > 83:
                # 在 filepathEN 中找到对应的图像
                filesEN = os.listdir(filepathEN)
                for fileEN in filesEN:
                    # 如果文件名以 BT1- 开头，并且第八个字符为点，则开始处理图片
                    if fileEN.startswith("BT1-") and fileEN[7] == ".":
                        # 读取 BT1- 开头的图像
                        imageEN = cv2.imread(os.path.join(filepathEN, fileEN))
                        # 取出 BT1- 后面的数字
                        numEN = fileEN[4:7]

                        # 如果两张图片的数字相同，且第七个元素为点
                        if numCN == numEN:
                            # 取出 imageEN 中指定高度和宽度的部分，并覆盖到 imageCN 中
                            imageCN[highStart:highEnd, wideStart:wideEnd] = imageEN[
                                highStart:highEnd, wideStart:wideEnd
                            ]

                            # 将 imageCN 保存到 destpath 中
                            cv2.imwrite(os.path.join(destpath, fileCN), imageCN)

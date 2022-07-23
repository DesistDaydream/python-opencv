import os
import cv2


def HandlerImage():
    # 在 filepathEN 中找到对应的图像
    filesEN = os.listdir(filepathEN)
    for fileEN in filesEN:
        # 如果文件名以 CardNamePrefix 定义的卡名开头，并且第八个字符为点，则开始处理图片
        if fileEN.startswith(CardNamePrefix) and fileEN[7] == ".":
            # 读取 CardNamePrefix 定义的卡名开头的图像
            imageEN = cv2.imread(os.path.join(filepathEN, fileEN))
            # 取出 CardNamePrefix 定义的卡名后面的数字
            numEN = fileEN[4:7]

            # 如果两张图片的数字相同，且第七个元素为点
            if numCN == numEN:
                # 取出 imageEN 中指定高度和宽度的部分，并覆盖到 imageCN 中
                imageCN[highStart:highEnd, wideStart:wideEnd] = imageEN[
                    highStart:highEnd, wideStart:wideEnd
                ]

                # 将 imageCN 保存到 destpath 中
                cv2.imwrite(os.path.join(destpath, fileCN), imageCN)


if __name__ == "__main__":
    # 确定卡片名称前缀，以便匹配图片
    CardNamePrefix = "BT2-"

    dirpathEN = "BT01-03"
    dirpahtCN = "BTC-01"
    destpath = "BT-02"

    # 判断当前系统是 windows 还是 linux
    if os.name == "posix":
        # 需要裁剪源图像
        filepathEN = "/mnt/e/Projects/DesistDaydream/dtcg/images/en/" + dirpathEN
        # 将裁剪的图像合并到这个目录下的图片
        filepathCN = "/mnt/e/Projects/DesistDaydream/dtcg/images/cn/" + dirpahtCN
        destpath = "/mnt/e/Projects/DesistDaydream/dtcg/images/cn-prefect/" + destpath
    elif os.name == "nt":
        # 需要裁剪源图像
        filepathEN = "E:\Projects\DesistDaydream\dtcg\images\en\\" + dirpathEN
        # 将裁剪的图像合并到这个目录下的图片
        filepathCN = "E:\Projects\DesistDaydream\dtcg\images\cn\\" + dirpahtCN
        destpath = "E:\Projects\DesistDaydream\dtcg\images\cn-prefect\\" + destpath
    else:
        print("未知操作系统")
        exit(1)

    # 逐一处理 filepathCN 中的图片
    filesCN = os.listdir(filepathCN)

    for fileCN in filesCN:
        # 如果图片的名称以 CardNamePrefix 定义的卡名开头，并且第八个字符为字母，则处理该图片
        if fileCN.startswith(CardNamePrefix) and fileCN[7].isalpha():
            # 读取 CardNamePrefix 定义的卡名开头的图像
            imageCN = cv2.imread(os.path.join(filepathCN, fileCN))
            # 取出 CardNamePrefix 定义的卡名后面的数字
            numCN = fileCN[4:7]

            # 数码宝贝与选项卡、驯兽师卡需要删除的水印高度不一样，根据实际情况，选择要处理的图片
            if int(numCN) <= 83 or int(numCN) >= 111:
                highStart = int(265)  # 高度起点
                highEnd = int(350)  # 高度终点(数码宝贝)
                wideStart = int(32)  # 宽度起点
                wideEnd = int(398)  # 宽度终点
                HandlerImage()
            elif int(numCN) >= 84 and int(numCN) <= 110:
                highStart = int(265)  # 高度起点
                highEnd = int(330)  # 高度终点(驯兽师、选项)
                wideStart = int(32)  # 宽度起点
                wideEnd = int(398)  # 宽度终点
                HandlerImage()

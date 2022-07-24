import os
import cv2
import logging


def HandlerImage():
    # 在 dirPahtEN 中找到对应的图像
    filesEN = os.listdir(dirPathEN)
    for fileEN in filesEN:
        # 如果文件名以 cardNamePrefix 定义的卡名开头，并且第八个字符为点，则开始处理图片
        if fileEN.startswith(cardNamePrefix) and fileEN[7] == ".":
            # 读取 cardNamePrefix 定义的卡名开头的图像
            imageEN = cv2.imread(os.path.join(dirPathEN, fileEN))
            # 取出 cardNamePrefix 定义的卡名后面的数字
            numEN = fileEN[4:7]

            # 如果两张图片的数字相同，且第七个元素为点
            if numCN == numEN:
                # 取出 imageEN 中指定高度和宽度的部分，并覆盖到 imageCN 中
                imageCN[highStart:highEnd, wideStart:wideEnd] = imageEN[
                    highStart:highEnd, wideStart:wideEnd
                ]

                # 将 imageCN 保存到 dirSuffixDst 中
                cv2.imwrite(os.path.join(dirSuffixDst, fileCN), imageCN)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %a %H:%M:%S",
        # filename="test.log",
        # filemode="w",
    )

    # 判断当前系统是 windows 还是 linux
    if os.name == "posix":
        dirPrefix = "/mnt/e/Projects/DesistDaydream/dtcg/images"
    elif os.name == "nt":
        dirPrefix = "E:\Projects\DesistDaydream\dtcg\images"
    else:
        print("未知操作系统")
        exit(1)

    dirSuffixCN = "STC-01"
    dirSuffixEN = "ST-1"
    dirSuffixDst = "ST-01"
    # 确定卡片名称前缀，以便匹配图片
    cardNamePrefix = "ST1-"

    # 需要将裁剪的图像合并到的图像的路径
    dirPathCN = os.path.join(dirPrefix, "cn", dirSuffixCN)
    # 需要裁剪的源图像路径
    dirPathEN = os.path.join(dirPrefix, "en", dirSuffixEN)
    # 合成之后的图像的保存路径
    dirPathDst = os.path.join(dirPrefix, "cn-prefect", dirSuffixDst)

    # 逐一处理 dirPathCN 中的图片
    filesCN = os.listdir(dirPathCN)

    # 确定卡包中数码宝贝的起始和结束卡号
    monNumStart = 12  # 数码宝贝小于该号
    monNumEnd = 16  # 数码宝贝大于该号
    # 确定卡包中驯兽师卡的起始和结束卡号
    tamerNumStart = 11  # 驯兽师和选项大于该号
    tamerNumEnd = 17  # 驯兽师和选项小于该号

    for fileCN in filesCN:
        # 如果图片的名称以 cardNamePrefix 定义的卡名开头，并且第八个字符为字母，则处理该图片
        if fileCN.startswith(cardNamePrefix) and fileCN[7].isalpha():
            # 读取 cardNamePrefix 定义的卡名开头的图像
            imageCN = cv2.imread(os.path.join(dirPathCN, fileCN))
            # 取出 cardNamePrefix 定义的卡名后面的数字
            numCN = fileCN[4:7]

            # 数码宝贝与选项卡、驯兽师卡需要删除的水印高度不一样，根据实际情况，选择要处理的图片
            if int(numCN) <= tamerNumStart or int(numCN) >= tamerNumEnd:
                highStart = int(265)  # 高度起点
                highEnd = int(350)  # 高度终点(数码宝贝)
                wideStart = int(32)  # 宽度起点
                wideEnd = int(398)  # 宽度终点
                HandlerImage()
            elif int(numCN) >= tamerNumStart and int(numCN) <= monNumEnd:
                highStart = int(265)  # 高度起点
                highEnd = int(330)  # 高度终点(驯兽师、选项)
                wideStart = int(32)  # 宽度起点
                wideEnd = int(398)  # 宽度终点
                HandlerImage()

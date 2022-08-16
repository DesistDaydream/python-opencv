#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import logging


def CheckCardNum(filePath, cardNum):
    if not cardNum.isdigit():
        logging.error("{} 的卡号 {} 不为正整数".format(filePath, cardNum))
        exit(1)


def HandlerImage():
    # 在 dirPahtEN 中找到对应的图像
    filesEN = os.listdir(dirPathEN)
    for fileEN in filesEN:
        # 如果文件名以 cardNamePrefix 定义的卡名开头，并且卡号末尾为点，则开始处理图片
        if (
            fileEN.startswith(filePrefixEN)
            and fileEN[len(filePrefixEN) + fileCardNumLenEN] == "."
        ):
            # 英文图片的绝对路径
            filePathEN = os.path.join(dirPathEN, fileEN)
            # 读取 cardNamePrefix 定义的卡名开头的图像
            imageEN = cv2.imread(filePathEN)
            # 获取文件名中的卡号，即文件名前缀的后面几位字符
            cardNumEN = fileEN[len(filePrefixEN) : len(filePrefixEN) + fileCardNumLenEN]
            # 若卡号不为正整数，则退出程序
            CheckCardNum(filePathEN, cardNumEN)

            # 如果两张图片的卡号相同
            if cardNumCN == cardNumEN:
                logging.debug("开始处理英文图片: {},卡片编号: {}".format(filePathEN, cardNumEN))
                # 取出 imageEN 中指定高度和宽度的部分，并覆盖到 imageCN 中
                imageCN[highStart:highEnd, wideStart:wideEnd] = imageEN[
                    highStart:highEnd, wideStart:wideEnd
                ]

                # 处理后图片的绝对路径
                filePathDst = os.path.join(dirPathDst, fileCN)
                # 递归创建目录
                if not os.path.exists(dirPathDst):
                    os.makedirs(dirPathDst)
                logging.debug("保存图片: {}".format(filePathDst))

                # 将 imageCN 保存到 dirSuffixDst 中
                cv2.imwrite(filePathDst, imageCN)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %a %H:%M:%S",
        # filename="test.log",
        # filemode="w",
    )

    # 判断当前系统是 windows 还是 linux
    if os.name == "posix":
        dirPrefix = "/mnt/e/Projects/dtcg/images"
    elif os.name == "nt":
        dirPrefix = "E:\Projects\dtcg\images"
    else:
        print("未知操作系统")
        exit(1)

    # 目录前缀。
    dirSuffixCN = "BTC-02"
    dirSuffixEN = "BT01-03"
    dirSuffixDst = "BT-03"
    # 图片名称前缀。用以匹配图片
    filePrefixCN = "BTC2_BT3-"
    filePrefixEN = "BT3-"
    # 图片中卡号的字符长度，指的是中文/英文的图片名称前缀后面的数字
    # 通常来说，预组的长度为2，扩展包的长度为3
    fileCardNumLenCN = 3
    fileCardNumLenEN = 3

    # 图片中的卡号中驯兽师、选项的起始和结束卡号
    fileCardNumOfTamerStart = 93  # 驯兽师和选项大于等于该号
    fileCardNumOfTamerEnd = 110  # 驯兽师和选项小于等于该号
    # 图片中的卡号中数码宝贝、数码蛋的起始和结束卡号
    fileCardNumOfDigimonStart = fileCardNumOfTamerStart - 1  # 数码宝贝小于等于该号
    fileCardNumOfDigimonEnd = fileCardNumOfTamerEnd + 1  # 数码宝贝大于等于该号

    # 需要将裁剪的图像合并到的图像的路径
    dirPathCN = os.path.join(dirPrefix, "cn", dirSuffixCN)
    # 需要裁剪的源图像路径
    dirPathEN = os.path.join(dirPrefix, "en", dirSuffixEN)
    # 合成之后的图像的保存路径
    dirPathDst = os.path.join(dirPrefix, "cn-prefect", dirSuffixDst)

    # 逐一处理 dirPathCN 中的图片
    filesCN = os.listdir(dirPathCN)
    logging.info("开始逐一处理【{}】开头的图片".format(filePrefixCN))
    logging.info("中文图片路径: 【{}】".format(dirPathCN))
    logging.info("英文图片路径: 【{}】".format(dirPathEN))
    logging.info("合成图片路径: 【{}】".format(dirPathDst))
    for fileCN in filesCN:
        # 如果图片的名称以 filePrefixCN 定义的卡名开头，则处理该图片
        if fileCN.startswith(filePrefixCN):
            # 如果图片的名称以 filePrefixCN 定义的卡名开头，并且卡号末尾为字母，则处理该图片
            # if (
            #     fileCN.startswith(filePrefixCN)
            #     and fileCN[len(filePrefixCN) + fileCardNumLenCN].isalpha()
            # ):
            # 中文图片的绝对路径
            filePathCN = os.path.join(dirPathCN, fileCN)

            # 读取 filePrefixCN 定义的卡名开头的图像
            imageCN = cv2.imread(filePathCN)
            # 获取文件名中的卡号，即文件名前缀的后面几位字符
            cardNumCN = fileCN[len(filePrefixCN) : len(filePrefixCN) + fileCardNumLenCN]
            # 若卡号不为正整数，则退出程序
            CheckCardNum(filePathCN, cardNumCN)

            # 数码宝贝与选项卡、驯兽师卡需要删除的水印高度不一样，根据实际情况，选择要处理的图片
            if (
                int(cardNumCN) <= fileCardNumOfDigimonStart
                or int(cardNumCN) >= fileCardNumOfDigimonEnd
            ):
                logging.debug(
                    "开始处理中文图片。数码宝贝/数码蛋图片: {},卡片编号: {}".format(filePathCN, cardNumCN)
                )
                highStart = int(265)  # 高度起点
                highEnd = int(350)  # 高度终点(数码宝贝)
                wideStart = int(32)  # 宽度起点
                wideEnd = int(398)  # 宽度终点
                HandlerImage()
            elif (
                int(cardNumCN) >= fileCardNumOfTamerStart
                and int(cardNumCN) <= fileCardNumOfTamerEnd
            ):
                logging.debug(
                    "开始处理中文图片。驯兽师/选项卡图片: {},卡片编号: {}".format(filePathCN, cardNumCN)
                )
                highStart = int(265)  # 高度起点
                highEnd = int(330)  # 高度终点(驯兽师、选项)
                wideStart = int(32)  # 宽度起点
                wideEnd = int(398)  # 宽度终点
                HandlerImage()
            else:
                logging.error("卡片编号【{}】不在处理范围内".format(cardNumCN))
        else:
            logging.error("【{}】图片没有匹配到【{}】前缀".format(fileCN, filePrefixCN))

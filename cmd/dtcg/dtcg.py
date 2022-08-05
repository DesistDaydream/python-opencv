#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import logging


def HandlerImage():
    # 在 dirPahtEN 中找到对应的图像
    filesEN = os.listdir(dirPathEN)
    for fileEN in filesEN:
        # 如果文件名以 cardNamePrefix 定义的卡名开头，并且卡号末尾为点，则开始处理图片
        if (
            fileEN.startswith(filePrefixEN)
            and fileEN[len(filePrefixEN) + fileCardNumLenEN] == "."
        ):
            # 英文图片绝对路径
            filePathEN = os.path.join(dirPathEN, fileEN)
            # 读取 cardNamePrefix 定义的卡名开头的图像
            imageEN = cv2.imread(filePathEN)
            # 获取文件名中的卡号，即文件名前缀的后面几位字符
            cardNumEN = fileEN[len(filePrefixEN) : len(filePrefixEN) + fileCardNumLenEN]

            # 如果两张图片的卡号相同
            if cardNumCN == cardNumEN:
                logging.debug("开始处理英文图片: {},卡片编号: {}".format(filePathEN, cardNumEN))
                # 取出 imageEN 中指定高度和宽度的部分，并覆盖到 imageCN 中
                imageCN[highStart:highEnd, wideStart:wideEnd] = imageEN[
                    highStart:highEnd, wideStart:wideEnd
                ]

                # 将 imageCN 保存到 dirSuffixDst 中
                filePathDst = os.path.join(dirPathDst, fileCN)
                # 递归创建目录
                if not os.path.exists(dirPathDst):
                    os.makedirs(dirPathDst)
                logging.debug("保存图片: {}".format(filePathDst))
                cv2.imwrite(filePathDst, imageCN)


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
        dirPrefix = "/mnt/d/Projects/DesistDaydream/dtcg/images"
    elif os.name == "nt":
        dirPrefix = "D:\Projects\DesistDaydream\dtcg\images"
    else:
        print("未知操作系统")
        exit(1)

    # 目录前缀。
    dirSuffixCN = "STC-02"
    dirSuffixEN = "ST-2"
    dirSuffixDst = "ST-02"
    # 图片名称前缀。用以匹配图片
    # 中文前缀
    filePrefixCN = "ST2-"
    # 英文前缀
    filePrefixEN = "ST2-"
    # 图片中卡号的字符长度
    # 中文长度
    fileCardNumLenCN = 2
    # 英文长度
    fileCardNumLenEN = 2
    # 图片中的卡号中数码宝贝、数码蛋的起始和结束卡号
    fileCardNumOfDigimonStart = 11  # 数码宝贝小于等于该号
    fileCardNumOfDigimonEnd = 18  # 数码宝贝大于等于该号
    # 图片中的卡号中驯兽师、选项的起始和结束卡号
    fileCardNumOfTamerStart = 12  # 驯兽师和选项大于等于该号
    fileCardNumOfTamerEnd = 16  # 驯兽师和选项小于等于该号

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
        # 如果图片的名称以 filePrefixCN 定义的卡名开头，并且卡号末尾为字母，则处理该图片
        # if fileCN.startswith(filePrefixCN) and fileCN[fileCardNumEndCN].isalpha():
        # 如果图片的名称以 filePrefixCN 定义的卡名开头，则处理该图片
        if fileCN.startswith(filePrefixCN):
            # 中文图片绝对路径
            filePathCN = os.path.join(dirPathCN, fileCN)

            # 读取 filePrefixCN 定义的卡名开头的图像
            imageCN = cv2.imread(filePathCN)
            # 获取文件名中的卡号，即文件名前缀的后面几位字符
            cardNumCN = fileCN[len(filePrefixCN) : len(filePrefixCN) + fileCardNumLenCN]

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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import logging


class CardsInfo:
    def __init__(self) -> None:
        # 目录前缀。
        self.dirSuffixCN: str = "EXC-01"
        self.dirSuffixEN: str = "EX2"
        self.dirSuffixDst: str = "EX-02"
        # 图片名称前缀。用以匹配图片
        self.filePrefixCN: str = "EX2-"
        self.filePrefixEN: str = "EX2-"
        # 图片中卡号的字符长度，指的是中文/英文的图片名称前缀后面的数字
        # 通常来说，预组的长度为2，扩展包的长度为3
        self.fileCardNumLenCN: int = 3
        self.fileCardNumLenEN: int = 3
        # 图片中的卡号中驯兽师、选项的起始和结束卡号
        self.fileCardNumOfTamerStart: int = 56
        self.fileCardNumOfTamerEnd: int = 72
        # 图片中的卡号中数码宝贝、数码蛋的起始和结束卡号
        self.fileCardNumOfDigimonStart: int = self.fileCardNumOfTamerStart - 1
        self.fileCardNumOfDigimonEnd: int = self.fileCardNumOfTamerEnd + 1

        # 数码宝贝/数码蛋图片
        self.highStart: int = 265  # 高度起点
        # highEnd = int(350)  # 高度终点(数码宝贝)
        self.highEnd: int = 337  # 高度终点(数码宝贝，带合体进化的描述)
        self.wideStart: int = 32  # 宽度起点
        self.wideEnd: int = 398  # 宽度终点
        # wideStart = int(15)  # 宽度起点(B站截图)
        # wideEnd = int(415)  # 宽度终点(B站截图)
        # 大图的像素点
        # highStart = int(550)  # 高度起点
        # highEnd = int(670)  # 高度终点(数码宝贝)
        # wideStart = int(69)  # 宽度起点
        # wideEnd = int(799)  # 宽度终点

        # 驯兽师/选项卡图片
        self.highStart: int = 265  # 高度起点
        self.highEnd: int = 330  # 高度终点(驯兽师、选项)
        self.wideStart: int = 32  # 宽度起点
        self.wideEnd: int = 398  # 宽度终点
        # wideStart = int(15)  # 宽度起点(B站截图)
        # wideEnd = int(415)  # 宽度终点(B站截图)


def HandlerImage(cardsInfo, dirPathEN, dirPathDst, cardNumCN, imageCN, fileCN):
    # 在 dirPahtEN 中找到对应的图像
    filesEN = os.listdir(dirPathEN)
    for fileEN in filesEN:
        # 如果文件名以 cardNamePrefix 定义的卡名开头，并且卡号末尾为点，则开始处理图片
        if (
            fileEN.startswith(cardsInfo.filePrefixEN)
            # and fileEN[len(filePrefixEN) + fileCardNumLenEN] == "."
        ):
            # 英文图片的绝对路径
            filePathEN = os.path.join(dirPathEN, fileEN)
            # 读取 cardNamePrefix 定义的卡名开头的图像
            imageEN = cv2.imread(filePathEN)
            # 获取文件名中的卡号，即文件名前缀的后面几位字符
            cardNumEN = fileEN[
                len(cardsInfo.filePrefixEN) : len(cardsInfo.filePrefixEN)
                + cardsInfo.fileCardNumLenEN
            ]
            # 若卡号不为正整数，则不处理该卡片，跳过
            if not CheckCardNum(filePathEN, cardNumEN):
                continue

            # 如果两张图片的卡号相同
            if cardNumCN == cardNumEN:
                logging.debug("开始处理英文图片: {},卡片编号: {}".format(filePathEN, cardNumEN))
                # 取出 imageEN 中指定高度和宽度的部分，并覆盖到 imageCN 中
                imageCN[
                    cardsInfo.highStart : cardsInfo.highEnd,
                    cardsInfo.wideStart : cardsInfo.wideEnd,
                ] = imageEN[
                    cardsInfo.highStart : cardsInfo.highEnd,
                    cardsInfo.wideStart : cardsInfo.wideEnd,
                ]

                # 处理后图片的绝对路径
                filePathDst = os.path.join(dirPathDst, fileCN)
                # 递归创建目录
                if not os.path.exists(dirPathDst):
                    os.makedirs(dirPathDst)
                logging.debug("保存图片: {}".format(filePathDst))

                # 将 imageCN 保存到 dirSuffixDst 中
                cv2.imwrite(filePathDst, imageCN)


def GenNeededHandleImage(cardsInfo, dirPathCN, dirPathEN, dirPathDst):
    # 逐一处理 dirPathCN 中的图片
    filesCN = os.listdir(dirPathCN)
    logging.info("开始逐一处理【{}】开头的图片".format(cardsInfo.filePrefixCN))
    logging.info("中文图片路径: 【{}】".format(dirPathCN))
    logging.info("英文图片路径: 【{}】".format(dirPathEN))
    logging.info("合成图片路径: 【{}】".format(dirPathDst))
    for fileCN in filesCN:
        # 如果图片的名称以 filePrefixCN 定义的卡名开头，则处理该图片
        if fileCN.startswith(cardsInfo.filePrefixCN):
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
            cardNumCN = fileCN[
                len(cardsInfo.filePrefixCN) : len(cardsInfo.filePrefixCN)
                + cardsInfo.fileCardNumLenCN
            ]
            # 若卡号不为正整数，则不处理该卡片，
            if not CheckCardNum(filePathCN, cardNumCN):
                continue

            # 数码宝贝与选项卡、驯兽师卡需要删除的水印高度不一样，根据实际情况，选择要处理的图片
            if (
                int(cardNumCN) <= cardsInfo.fileCardNumOfDigimonStart
                or int(cardNumCN) >= cardsInfo.fileCardNumOfDigimonEnd
            ):
                logging.debug(
                    "开始处理中文图片。数码宝贝/数码蛋图片: {},卡片编号: {}".format(filePathCN, cardNumCN)
                )

                HandlerImage(
                    cardsInfo, dirPathEN, dirPathDst, cardNumCN, imageCN, fileCN
                )
            elif (
                int(cardNumCN) >= cardsInfo.fileCardNumOfTamerStart
                and int(cardNumCN) <= cardsInfo.fileCardNumOfTamerEnd
            ):
                logging.debug(
                    "开始处理中文图片。驯兽师/选项卡图片: {},卡片编号: {}".format(filePathCN, cardNumCN)
                )

                HandlerImage(
                    cardsInfo, dirPathEN, dirPathDst, cardNumCN, imageCN, fileCN
                )
            else:
                logging.error("卡片编号【{}】不在处理范围内".format(cardNumCN))
        else:
            logging.error("【{}】图片没有匹配到【{}】前缀".format(fileCN, cardsInfo.filePrefixCN))


def run(dirPrefix: str):
    cardsInfo = CardsInfo()

    # 需要将裁剪的图像合并到的图像的路径
    dirPathCN = os.path.join(dirPrefix, "cn", cardsInfo.dirSuffixCN)
    # 需要裁剪的源图像路径
    dirPathEN = os.path.join(dirPrefix, "en", cardsInfo.dirSuffixEN)
    # 合成之后的图像的保存路径
    dirPathDst = os.path.join(dirPrefix, "cn-prefect", cardsInfo.dirSuffixDst)

    GenNeededHandleImage(cardsInfo, dirPathCN, dirPathEN, dirPathDst)


def CheckCardNum(filePath, cardNum) -> bool:
    if cardNum.isdigit():
        return True
    else:
        logging.error("{} 的卡号 {} 不为正整数".format(filePath, cardNum))
        return False


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
        dirPrefix: str = "/mnt/d/Projects/dtcg/images"
    elif os.name == "nt":
        dirPrefix: str = "D:\\Projects\\dtcg\\images"
    else:
        print("未知操作系统")
        exit(1)

    run(dirPrefix)

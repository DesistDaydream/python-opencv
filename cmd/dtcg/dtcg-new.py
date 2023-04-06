#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import logging
import re


class CardsInfo:
    def __init__(self) -> None:
        # 目录前缀。
        self.dirPrefixCN: str = "EXC-01"
        self.dirPrefixEN: str = "EX2"
        self.dirPrefixDst: str = "EX-02"
        # 图片名称前缀。用以匹配图片
        self.filePrefixCN: str = "EX2-"
        self.filePrefixEN: str = "EX2-"
        # 图片名称后缀。用以匹配图片
        self.fileSuffixCN: str = ".png"
        self.fileSuffixEN: str = "_dummy.jpg"
        # 异画图片名称后缀。用以匹配图片
        # TODO: 如果有多张异画怎么办呢？多张异画的话，每种异画的后缀是不一样的。
        self.fileArtSuffixCN: str = "_01"
        self.fileArtSuffixEN: str = "P"
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

        # 图片存放路径
        # 需要将裁剪的图像合并到的图像的路径
        self.dirPathCN: str
        # 需要裁剪的源图像路径
        self.dirPathEN: str
        # 合成之后的图像的保存路径
        self.dirPathDst: str

        # 数码宝贝/数码蛋图片
        self.highStart: int  # 高度起点
        self.highEnd: int  # 高度终点(数码宝贝，带合体进化的描述)
        self.wideStart: int  # 宽度起点
        self.wideEnd: int  # 宽度终点

        # 驯兽师/选项卡图片
        self.highStart: int  # 高度起点
        self.highEnd: int  # 高度终点(驯兽师、选项)
        self.wideStart: int  # 宽度起点
        self.wideEnd: int  # 宽度终点

        # TODO: 我想加个卡牌类型的数据，然后能自动获取这个图片的卡牌类型，然后根据类型来决定裁剪的区域。但是如何获取到卡牌的类型呢？

    def SetWatermarkAreaCoordinates(self, cardType):
        if cardType == "digimon" or cardType == "digi-egg":
            # 数码宝贝/数码蛋图片
            self.highStart: int = 265  # 高度起点
            # highEnd = int(350)  # 高度终点(数码宝贝)
            self.highEnd: int = 337  # 高度终点(数码宝贝，带合体进化的描述)
            self.wideStart: int = 32  # 宽度起点
            self.wideEnd: int = 398  # 宽度终点
        elif cardType == "tamer" or cardType == "option":
            # 驯兽师/选项卡图片
            self.highStart: int = 265  # 高度起点
            self.highEnd: int = 329  # 高度终点(驯兽师、选项)
            self.wideStart: int = 32  # 宽度起点
            self.wideEnd: int = 398  # 宽度终点

    def GenDirPath(self, dirPrefix):
        # 需要将裁剪的图像合并到的图像的路径
        self.dirPathCN = os.path.join(dirPrefix, "cn", self.dirPrefixCN)
        # 需要裁剪的源图像路径
        self.dirPathEN = os.path.join(dirPrefix, "en", self.dirPrefixEN)
        # 合成之后的图像的保存路径
        self.dirPathDst = os.path.join(dirPrefix, "cn-prefect", self.dirPrefixDst)

        logging.info("中文图片路径: 【{}】".format(self.dirPathCN))
        logging.info("英文图片路径: 【{}】".format(self.dirPathEN))
        logging.info("合成图片路径: 【{}】".format(self.dirPathDst))

    def GenFileEN(self, cardNumCN):
        # 处理英文图片文件名称
        fileEN = self.filePrefixEN + cardNumCN + self.fileSuffixEN
        # 如果是名称超过卡号字符长度，则说明是异画，需要替换异画后缀
        if len(cardNumCN) > self.fileCardNumLenCN:
            fileEN = fileEN.replace(self.fileArtSuffixCN, self.fileArtSuffixEN)
        return fileEN

    def HandlerImage(
        self,
        dirPathEN: str,
        dirPathDst: str,
        cardNumCN: str,
        imageCN: cv2.Mat,
        fileCN: str,
    ):
        fileEN = self.GenFileEN(cardNumCN)
        # 如果目录中存在的英文图片文件，则处理
        if fileEN in os.listdir(dirPathEN):
            # 英文图片的绝对路径
            filePathEN = os.path.join(dirPathEN, fileEN)
            # 读取 cardNamePrefix 定义的卡名开头的图像
            imageEN = cv2.imread(filePathEN)

            logging.debug("开始处理英文图片: {},卡片编号: {}".format(filePathEN, cardNumCN))
            # 取出 imageEN 中指定高度和宽度的部分，并覆盖到 imageCN 中
            imageCN[
                self.highStart : self.highEnd,
                self.wideStart : self.wideEnd,
            ] = imageEN[
                self.highStart : self.highEnd,
                self.wideStart : self.wideEnd,
            ]

            # 处理后图片的绝对路径
            filePathDst = os.path.join(dirPathDst, fileCN)
            # 递归创建目录
            if not os.path.exists(dirPathDst):
                os.makedirs(dirPathDst)
            logging.debug("保存图片: {}".format(filePathDst))

            # 将 imageCN 保存到 dirSuffixDst 中
            cv2.imwrite(filePathDst, imageCN)

    def GenNeededHandleImage(self):
        logging.info("开始逐一处理【{}】开头的图片".format(self.filePrefixCN))

        # 逐一处理 dirPathCN 中的图片
        filesCN = os.listdir(self.dirPathCN)
        for fileCN in filesCN:
            # 如果图片的名称以 filePrefixCN 定义的卡名开头，则处理该图片
            if fileCN.startswith(self.filePrefixCN):
                # 中文图片的绝对路径
                filePathCN = os.path.join(self.dirPathCN, fileCN)
                # 读取 filePrefixCN 定义的卡名开头的图像
                imageCN = cv2.imread(filePathCN)
                # 获取文件名中的卡号
                cardNumCN = fileCN.replace(self.filePrefixCN, "").replace(
                    self.fileSuffixCN, ""
                )

                # 数码宝贝与选项卡、驯兽师卡需要删除的水印高度不一样，根据实际情况，选择要处理的图片
                if (
                    int(cardNumCN[: self.fileCardNumLenCN])
                    <= self.fileCardNumOfDigimonStart
                    or int(cardNumCN[: self.fileCardNumLenCN])
                    >= self.fileCardNumOfDigimonEnd
                ):
                    logging.debug(
                        "开始处理中文图片。数码宝贝/数码蛋图片: {},卡片编号: {}".format(filePathCN, cardNumCN)
                    )

                    self.SetWatermarkAreaCoordinates("digimon")

                    self.HandlerImage(
                        self.dirPathEN, self.dirPathDst, cardNumCN, imageCN, fileCN
                    )
                elif (
                    int(cardNumCN[: self.fileCardNumLenCN])
                    >= self.fileCardNumOfTamerStart
                    and int(cardNumCN[: self.fileCardNumLenCN])
                    <= self.fileCardNumOfTamerEnd
                ):
                    logging.debug(
                        "开始处理中文图片。驯兽师/选项卡图片: {},卡片编号: {}".format(filePathCN, cardNumCN)
                    )

                    self.SetWatermarkAreaCoordinates("tamer")

                    self.HandlerImage(
                        self.dirPathEN, self.dirPathDst, cardNumCN, imageCN, fileCN
                    )
                else:
                    logging.error("卡片编号【{}】不在处理范围内".format(cardNumCN))
            else:
                logging.error("【{}】图片没有匹配到【{}】前缀".format(fileCN, self.filePrefixCN))


def run(dirPrefix: str):
    cardsInfo = CardsInfo()

    cardsInfo.GenDirPath(dirPrefix)

    cardsInfo.GenNeededHandleImage()


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
        dirPrefix: str = "/mnt/d/Projects/dtcg/images"
    elif os.name == "nt":
        dirPrefix: str = "D:\\Projects\\dtcg\\images"
    else:
        print("未知操作系统")
        exit(1)

    run(dirPrefix)

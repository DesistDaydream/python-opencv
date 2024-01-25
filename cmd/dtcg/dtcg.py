#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import logging
from typing import Dict, List

from dataclasses import dataclass


# 图片存放路径
# 需要将裁剪的图像合并到的图像的路径
dirPathCN: str
# 需要裁剪的源图像路径
dirPathEN: str
# 合成之后的图像的保存路径
dirPathDst: str

# 目录前缀。
dirPrefixCN: str = "EXC-03"
dirPrefixEN: str = "EX-05"
dirPrefixDst: str = "EX-05"
# 图片名称前缀。用以匹配图片以及生成卡牌编号
filePrefixCN: str = "EX5-"
filePrefixEN: str = "EX5-"
# 图片名称后缀。用以匹配图片以及生成卡牌编号
fileSuffixCN: str = ".png"
fileSuffixEN: str = ".png"
# 异画图片名称后缀。用以匹配图片
# TODO: 如果有多张异画怎么办呢？多张异画的话，每种异画的后缀是不一样的。
fileArtSuffixCN: str = "_P1"
fileArtSuffixEN: str = "_P1"
# 图片中卡号的字符长度，指的是中文/英文的图片名称前缀后面的数字
# 通常来说，预组的长度为2，扩展包的长度为3
fileCardNumLenCN: int = 3
fileCardNumLenEN: int = 3
# 图片中的卡号中驯兽师、选项的起始和结束卡号
fileCardNumOfTamerStart: int = 64
fileCardNumOfTamerEnd: int = 72
# 图片中的卡号中数码宝贝、数码蛋的起始和结束卡号
fileCardNumOfDigimonStart: int = fileCardNumOfTamerStart - 1
fileCardNumOfDigimonEnd: int = fileCardNumOfTamerEnd + 1


# 生成各种工作路径
def GenDirPath(dirPrefix: str):
    global dirPathCN, dirPathEN, dirPathDst
    # 需要将裁剪的图像合并到的图像的路径
    dirPathCN = os.path.join(dirPrefix, "cn", dirPrefixCN)
    # 需要裁剪的源图像路径
    dirPathEN = os.path.join(dirPrefix, "jp", dirPrefixEN)
    # 合成之后的图像的保存路径
    dirPathDst = os.path.join(dirPrefix, "cn-prefect", dirPrefixDst)

    logging.info("中文图片路径: 【{}】".format(dirPathCN))
    logging.info("英文图片路径: 【{}】".format(dirPathEN))
    logging.info("合成图片路径: 【{}】".format(dirPathDst))


@dataclass
class WatermarkArea:
    highStart: int
    highEnd: int
    wideStart: int
    wideEnd: int


def SetWatermarkAreaCoordinates(cardType: str) -> WatermarkArea:
    if cardType == "digimon" or cardType == "digi-egg":
        # 数码宝贝/数码蛋图片
        highStart: int = 265  # 高度起点
        # highEnd = int(350)  # 高度终点(数码宝贝)
        highEnd: int = 332  # 高度终点(数码宝贝，带合体进化的描述)
        wideStart: int = 32  # 宽度起点
        wideEnd: int = 398  # 宽度终点

        return WatermarkArea(highStart, highEnd, wideStart, wideEnd)
    elif cardType == "tamer" or cardType == "option":
        # 驯兽师/选项卡图片
        highStart: int = 265  # 高度起点
        highEnd: int = 329  # 高度终点(驯兽师、选项)
        wideStart: int = 32  # 宽度起点
        wideEnd: int = 398  # 宽度终点

        return WatermarkArea(highStart, highEnd, wideStart, wideEnd)

    print("请指定卡牌类型！")
    exit(1)


@dataclass
class cardTypesInfo:
    cardsSerial: List[str]  # 当前卡牌类型下的所有卡牌编号列表
    watermarkArea: WatermarkArea  # 水印区域的坐标


@dataclass
class imageHandler:
    cardTypesInfo: Dict[str, cardTypesInfo]

    # 处理图片
    def HandlingImage(self):
        # 列出日/英语目录下的所有卡牌文件
        filesEN = os.listdir(dirPathEN)

        for type, cardTypesInfo in self.cardTypesInfo.items():
            for fileCN in cardTypesInfo.cardsSerial:
                # 提取卡牌的纯数字编号
                cardNumCN = fileCN.replace(filePrefixCN, "").replace(fileSuffixCN, "")
                fileEN = GenFileEN(cardNumCN)

                # 如果目录中存在日/英语的图片文件，则处理
                if fileEN in filesEN:
                    logging.debug("开始处理英文图片: {},卡片编号: {}".format(fileEN, cardNumCN))

                    # 中文图片的绝对路径
                    filePathCN = os.path.join(dirPathCN, fileCN)
                    # 读取 filePrefixCN 定义的卡名开头的图像
                    imageCN = cv2.imread(filePathCN)
                    # 日/英语图片的绝对路径
                    filePathEN = os.path.join(dirPathEN, fileEN)
                    # 读取 cardNamePrefix 定义的卡名开头的图像
                    imageEN = cv2.imread(filePathEN)

                    # 取出 imageEN 中指定高度和宽度的部分，并覆盖到 imageCN 中
                    imageCN[
                        cardTypesInfo.watermarkArea.highStart : cardTypesInfo.watermarkArea.highEnd,
                        cardTypesInfo.watermarkArea.wideStart : cardTypesInfo.watermarkArea.wideEnd,
                    ] = imageEN[
                        cardTypesInfo.watermarkArea.highStart : cardTypesInfo.watermarkArea.highEnd,
                        cardTypesInfo.watermarkArea.wideStart : cardTypesInfo.watermarkArea.wideEnd,
                    ]

                    # 处理后图片的绝对路径
                    filePathDst = os.path.join(dirPathDst, fileCN)
                    # 递归创建目录
                    if not os.path.exists(dirPathDst):
                        os.makedirs(dirPathDst)

                    logging.debug("保存图片: {}".format(filePathDst))

                    # 将 imageCN 保存到 dirSuffixDst 中
                    cv2.imwrite(filePathDst, imageCN)
                else:
                    logging.error("【{}】图片没有匹配到【{}】".format(fileCN, fileEN))


# 生成英文图片文件名称
def GenFileEN(cardNumCN: str):
    # 处理英文图片文件名称
    fileEN: str = filePrefixEN + cardNumCN + fileSuffixEN
    # 如果是名称超过卡号字符长度，则说明是异画，需要替换异画后缀
    if len(cardNumCN) > fileCardNumLenCN:
        fileEN = fileEN.replace(fileArtSuffixCN, fileArtSuffixEN)
    return fileEN


def NewImageHandler() -> imageHandler:
    logging.info("开始逐一处理【{}】开头的图片".format(filePrefixCN))

    h = imageHandler({})
    digimonCard = []
    tamerCard = []

    # TODO: 我想加个卡牌类型的数据，然后能自动获取这个图片的卡牌类型，然后根据类型来决定裁剪的区域。但是如何获取到卡牌的类型呢？
    # 逐一处理 dirPathCN 中的图片
    filesCN = os.listdir(dirPathCN)
    for fileCN in filesCN:
        # 如果图片的名称以 filePrefixCN 定义的卡名开头，则处理该图片
        if fileCN.startswith(filePrefixCN):
            # 获取文件名中的卡号
            cardNumCN = fileCN.replace(filePrefixCN, "").replace(fileSuffixCN, "")

            # 数码宝贝与选项卡、驯兽师卡需要删除的水印高度不一样，根据实际情况，选择要处理的图片
            if int(cardNumCN[:fileCardNumLenCN]) <= fileCardNumOfDigimonStart or int(cardNumCN[:fileCardNumLenCN]) >= fileCardNumOfDigimonEnd:
                digimonCard.append(fileCN)
            elif int(cardNumCN[:fileCardNumLenCN]) >= fileCardNumOfTamerStart and int(cardNumCN[:fileCardNumLenCN]) <= fileCardNumOfTamerEnd:
                tamerCard.append(fileCN)
            else:
                logging.error("卡片编号【{}】不在处理范围内".format(cardNumCN))
        else:
            logging.error("【{}】图片没有匹配到【{}】前缀".format(fileCN, filePrefixCN))

    for type in ["digimon", "tamer"]:
        i = cardTypesInfo(
            cardsSerial=digimonCard if type == "digimon" else tamerCard,
            watermarkArea=SetWatermarkAreaCoordinates(type),
        )
        h.cardTypesInfo[type] = i

    logging.debug(h.cardTypesInfo["digimon"].cardsSerial)
    logging.debug(h.cardTypesInfo["tamer"].cardsSerial)

    return h


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

    GenDirPath(dirPrefix)

    cardsInfo = NewImageHandler()
    cardsInfo.HandlingImage()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import logging
import click


@click.command()
@click.option("--serial", prompt="卡牌编号", default="BT10-009", help="卡牌编号")
def run(serial: str):
    # 数码宝贝/数码蛋图片
    # highStart: int = 265  # 高度起点
    # highEnd: int = 332  # 高度终点(数码宝贝，带合体进化的描述)
    # wideStart: int = 30  # 宽度起点
    # wideEnd: int = 400  # 宽度终点

    # 驯兽师/选项卡图片
    highStart: int = 265  # 高度起点
    highEnd: int = 330  # 高度终点(驯兽师、选项)
    wideStart: int = 32  # 宽度起点
    wideEnd: int = 398  # 宽度终点

    cnFile = "cn/P/{}.png".format(serial)
    jpFile = "en/P/{}.png".format(serial)
    dstFile = "cn-prefect/P/{}.png".format(serial)
    # cnFile = "cn/BTC-05/{}_01.png".format(serial)
    # jpFile = "jp_hk/BT-10/{}_P1.png".format(serial)
    # dstFile = "cn-prefect/BT-10/{}_01.png".format(serial)

    filePathCN = os.path.join(dirPrefix, cnFile)
    filePathJP = os.path.join(dirPrefix, jpFile)
    filePathDst = os.path.join(dirPrefix, dstFile)

    imageCN = cv2.imread(filePathCN)
    imageJP = cv2.imread(filePathJP)
    imageCN[
        highStart:highEnd,
        wideStart:wideEnd,
    ] = imageJP[
        highStart:highEnd,
        wideStart:wideEnd,
    ]

    # 将 imageCN 保存到 dirSuffixDst 中
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
        dirPrefix: str = "/mnt/d/Projects/dtcg/images"
    elif os.name == "nt":
        dirPrefix: str = "D:\\Projects\\dtcg\\images"
    else:
        print("未知操作系统")
        exit(1)

    run()

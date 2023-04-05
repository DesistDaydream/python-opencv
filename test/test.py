#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re


def match_files(dir_a: str, dir_b: str, cardNamePrefix: str):
    for filename_a in os.listdir(dir_a):
        new_name = filename_a.replace(cardNamePrefix, "").replace(".png", "")
        print(new_name)


dir_a = "D:\\Projects\\dtcg\\images\\cn\\EXC-01"
dir_b = "D:\\Projects\\dtcg\\images\\en\\EX2"
# Replace AA and BB with your directory names
match_files(dir_a, dir_b, "EX2-")

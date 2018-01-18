# -*- coding: utf-8 -*-


"""

dynamic command line output

"""
import os
import sys
import platform

from terminaltables import AsciiTable

BAIDU_SEARCH = 1
KNOWLEDGE_MAP = 2
QUESTION = 0

MAX_TEXT_WIDTH = 45


def clear_screen():
    system_version = platform.system().upper()
    if system_version.startswith("LINUX"):
        os.system("clear")
    if system_version.startswith("WINDOWS"):
        os.system("cls")
    if system_version.startswith("DARWIN"):
        os.system("clear")


def print_terminal(readpipe):
    """
    pipe item struct
    - type
    - data
    
    :param readpipe: 
    :return: 
    """
    baidu_search = ""
    knowledge_map = ""
    question = ""
    time_duration = ""

    while True:
        item = readpipe.get()
        if item["type"] == 0:
            question = item["data"]
        if item["type"] == 1:
            baidu_search = item["data"]
        elif item["type"] == 2:
            knowledge_map = item["data"]
        elif item["type"] == 3:
            time_duration = item["data"]
        elif item["type"] == 4:
            print(item["data"])
            sys.stdout.flush()
            continue
        data = [
            ["问题", question],
            ["百度决策", baidu_search],
            ["知识图谱", knowledge_map],
            ["耗时", time_duration]
        ]
        table = AsciiTable(table_data=data)
        table.inner_row_border = True
        clear_screen()
        print(table.table)
        sys.stdout.flush()

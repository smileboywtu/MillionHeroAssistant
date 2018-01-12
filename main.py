# -*- coding:utf-8 -*-


"""

    Xi Gua video Million Heroes

"""
import time
from argparse import ArgumentParser

import operator
from functools import partial
from terminaltables import AsciiTable

from config import api_key
from config import api_version
from config import app_id
from config import app_key
from config import app_secret
from config import data_directory
from config import hanwan_appcode
from config import image_compress_level
from config import prefer
from core.android import analyze_current_screen_text
from core.android import save_screen
from core.baiduzhidao import baidu_count
from core.check_words import parse_false
from core.ocr.baiduocr import get_text_from_image as bai_get_text
from core.ocr.hanwanocr import get_text_from_image as han_get_text
from core.ocr.spaceocr import get_text_from_image as ocrspace_get_text

if prefer[0] == "baidu":
    get_text_from_image = partial(bai_get_text,
                                  app_id=app_id,
                                  app_key=app_key,
                                  app_secret=app_secret,
                                  api_version=api_version,
                                  timeout=5)
elif prefer[0] == "hanwang":
    get_text_from_image = partial(han_get_text, appcode=hanwan_appcode, timeout=3)

elif prefer[0] == "ocrspace":
    get_test_from_image = partial(ocrspace_get_text, api_key=api_key)


def parse_args():
    parser = ArgumentParser(description="Million Hero Assistant")
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=5,
        help="default http request timeout"
    )
    return parser.parse_args()


def parse_question_and_answer(text_list):
    question = ""
    start = 0
    for i, keyword in enumerate(text_list):
        question += keyword
        if "?" in keyword:
            start = i + 1
            break
    question = question.split(".")[-1]
    question, true_flag = parse_false(question)
    return true_flag, question, text_list[start:]


def pre_process_question(keyword):
    """
    strip charactor and strip ?
    :param question:
    :return:
    """
    for char, repl in [("“", ""), ("”", ""), ("？", "")]:
        keyword = keyword.replace(char, repl)

    keyword = keyword.split(r"．")[-1]
    keywords = keyword.split(" ")
    keyword = "".join([e.strip("\r\n") for e in keywords if e])
    return keyword


def main():
    args = parse_args()
    timeout = args.timeout

    def __inner_job():
        start = time.time()
        text_binary = analyze_current_screen_text(
            directory=data_directory,
            compress_level=image_compress_level[0]
        )
        keywords = get_text_from_image(
            image_data=text_binary,
        )
        if not keywords:
            print("text not recognize")
            return

        true_flag, question, answers = parse_question_and_answer(keywords)
        print('-' * 72)
        print(question)
        print('-' * 72)
        print("\n".join(answers))

        search_question = pre_process_question(question)
        summary = baidu_count(search_question, answers, timeout=timeout)
        summary_li = sorted(summary.items(), key=operator.itemgetter(1), reverse=True)
        data = [("选项", "同比")]
        for a, w in summary_li:
            data.append((a, w))
        table = AsciiTable(data)
        print(table.table)

        print("*" * 72)
        if true_flag:
            print("肯定回答(**)： ", summary_li[0][0])
            print("否定回答(  )： ", summary_li[-1][0])
        else:
            print("肯定回答(  )： ", summary_li[0][0])
            print("否定回答(**)： ", summary_li[-1][0])
        print("*" * 72)

        end = time.time()
        print("use {0} 秒".format(end - start))
        save_screen(
            directory=data_directory
        )

    while True:
        print("""
    请在答题开始前就运行程序，
    答题开始的时候按Enter预测答案
                """)

        enter = input("按Enter键开始，按ESC键退出...")
        if enter == chr(27):
            break
        try:
            __inner_job()
        except Exception as e:
            print(str(e))

        print("欢迎下次使用")


if __name__ == "__main__":
    main()

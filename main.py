# -*- coding:utf-8 -*-


"""

    Xi Gua video Million Heroes

"""
import time
from argparse import ArgumentParser

import operator
from functools import partial
from terminaltables import SingleTable

from config import api_version
from config import app_id
from config import app_key
from config import app_secret
from config import data_directory
from config import image_compress_level
from core.android import analyze_current_screen_text, save_screen
from core.nearby import calculate_relation
from core.nlp.word_analyze import analyze_keyword_from_question
from core.ocr.baiduocr import get_text_from_image as bai_get_text
from core.utils import save_question_answers_to_file, number_normalize


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
    return question, text_list[start:]


def main():
    args = parse_args()
    timeout = args.timeout
    get_text_from_image = partial(
        bai_get_text,
        app_id=app_id,
        app_key=app_key,
        app_secret=app_secret,
        api_version=api_version,
        timeout=timeout)

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

        question, answers = parse_question_and_answer(keywords)
        print('-' * 72)
        print(question)
        print('-' * 72)
        print("\n".join(answers))

        search_question = analyze_keyword_from_question(question)
        weight_li, final, index = calculate_relation(search_question, answers)
        min_member = min(weight_li)
        max_member = max(weight_li)
        normalize = partial(number_normalize,
                            max_member=max_member,
                            min_member=min_member,
                            c=100)
        summary = {
            a: b
            for a, b in
            zip(answers, weight_li)
        }
        summary_li = sorted(summary.items(), key=operator.itemgetter(1), reverse=True)
        data = [("选项", "同比")]
        for a, w in summary_li:
            data.append((a, "{:.3f}".format(normalize(w) if max_member > min_member else w)))
        table = SingleTable(data)
        print(table.table)

        print("*" * 72)
        print("肯定回答： ", summary_li[0][0])
        print("否定回答： ", summary_li[-1][0])
        print("*" * 72)

        end = time.time()
        print("use {0} 秒".format(end - start))

        save_screen(directory=data_directory)
        save_question_answers_to_file(question, answers, directory=data_directory)

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

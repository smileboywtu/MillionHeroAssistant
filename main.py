# -*- coding:utf-8 -*-


"""

    Xi Gua video Million Heroes

"""


import multiprocessing
from multiprocessing import Event
from multiprocessing import Pipe

import time
from argparse import ArgumentParser
from multiprocessing import Value

import operator
from functools import partial
from terminaltables import AsciiTable

from config import api_key
from config import api_version
from config import app_id
from config import app_key
from config import app_secret
from config import data_directory
from config import enable_chrome
from config import image_compress_level
from config import prefer
from core.android import analyze_current_screen_text
from core.android import save_screen
from core.baiduzhidao import baidu_count
from core.check_words import parse_false
from core.chrome_search import run_browser
from core.ocr.baiduocr import get_text_from_image as bai_get_text
from core.ocr.spaceocr import get_text_from_image as ocrspace_get_text

if prefer[0] == "baidu":
    get_text_from_image = partial(bai_get_text,
                                  app_id=app_id,
                                  app_key=app_key,
                                  app_secret=app_secret,
                                  api_version=api_version,
                                  timeout=5)

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
    real_question = question.split(".")[-1]
    question, true_flag = parse_false(real_question)
    return true_flag, real_question, question, text_list[start:]


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

    if enable_chrome:
        closer = Event()
        noticer = Event()
        closer.clear()
        noticer.clear()
        reader, writer = Pipe()
        browser_daemon = multiprocessing.Process(
            target=run_browser, args=(closer, noticer, reader,))
        browser_daemon.daemon = True
        browser_daemon.start()

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

        true_flag, real_question, question, answers = parse_question_and_answer(keywords)
        print('-' * 72)
        print(real_question)
        print('-' * 72)
        print("\n".join(answers))

        # notice browser
        if enable_chrome:
            writer.send(question)
            noticer.set()

        search_question = pre_process_question(question)
        summary = baidu_count(search_question, answers, timeout=timeout)
        summary_li = sorted(
            summary.items(), key=operator.itemgetter(1), reverse=True)
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

<<<<<<< HEAD
##############################################################
        input_message = question

        if len(input_message) > 60:
            print(mybot.respond("句子长度过长"))
        elif input_message.strip() == '':
            print(mybot.respond("无"))

        #print(input_message)
        message = T.wordSegment(input_message)
        # 去标点
        #print('word Seg:' + message)
        #print('词性：')
        words = T.postag(input_message)

        if message == 'q':
            exit()
        else:
            response = mybot.respond(message)

            #print("=======")
            #print(response)
            #print("=======")

            if response == "":
                ans = mybot.respond('找不到答案')
                print('Eric：' + ans)
            # 百科搜索
            elif response[0] == '#':
                # 匹配百科
                if response.__contains__("searchbaike"):
                    #print("searchbaike")
                    #print(response)
                    res = response.split(':')
                    # 实体
                    entity = str(res[1]).replace(" ", "")
                    # 属性
                    attr = str(res[2]).replace(" ", "")
                    #print(entity + '<---->' + attr)

                    ans = baike.query(entity, attr)
                    # 如果命中答案
                    if type(ans) == list:
                        print('Eric：' + QAT.ptranswer(ans, False))

                    elif ans.decode('utf-8').__contains__(u'::找不到'):
                        # 百度摘要+Bing摘要
                        print("通用搜索")
                        ans = search_summary.kwquery(input_message)

                # 匹配不到模版，通用查询
                elif response.__contains__("NoMatchingTemplate"):
                    #print("NoMatchingTemplate")
                    ans = search_summary.kwquery(input_message,answers)

                if len(ans) == 0:
                    print('Eric：' +'找不到答案')
                elif len(ans) > 1:
                    print("不确定候选答案")
                    print('Eric: ')
                    for a in ans:
                        print(a)
                else:
                    print('Eric：' + ans[0])



            # 匹配模版
            else:
                print('Eric：' + response)






=======
>>>>>>> parent of 74c2f45... Integrated QA question and answer
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

    if enable_chrome:
        reader.close()
        writer.close()
        closer.set()
        time.sleep(3)


if __name__ == "__main__":
    main()

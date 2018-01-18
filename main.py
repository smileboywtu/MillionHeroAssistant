# -*- coding:utf-8 -*-


"""

    Xi Gua video Million Heroes

"""
import multiprocessing
import operator
import os
import time
from argparse import ArgumentParser
from datetime import datetime
from functools import partial
<<<<<<< HEAD
from multiprocessing import Queue, Event, Pipe
from PIL import Image
=======
from multiprocessing import Event, Pipe
from textwrap import wrap

>>>>>>> upstream/master
from config import api_key, enable_chrome, use_monitor, image_compress_level, crop_areas
from config import api_version
from config import app_id
from config import app_key
from config import app_secret
from config import data_directory
from config import prefer
from core.android import save_screen, check_screenshot, get_adb_tool, analyze_current_screen_text,get_area_data
from core.check_words import parse_false
from core.chrome_search import run_browser
from core.crawler.baiduzhidao import baidu_count
from core.crawler.crawl import jieba_initialize, kwquery
from core.ocr.baiduocr import get_text_from_image as bai_get_text
from core.ocr.spaceocr import get_text_from_image as ocrspace_get_text
## jieba init
from dynamic_table import clear_screen

jieba_initialize()

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

    for char, repl in [("以下", ""), ("下列", "")]:
        real_question = real_question.replace(char, repl, 1)

    question, true_flag = parse_false(real_question)
    return true_flag, real_question, question, text_list[start:]


def pre_process_question(keyword):
    """
    strip charactor and strip ?
    :param question:
    :return:
    """
    now = datetime.today()
    for char, repl in [("“", ""), ("”", ""), ("？", ""), ("《", ""), ("》", ""), ("我国", "中国"),
                       ("今天", "{0}年{1}月{2}日".format(now.year, now.month, now.day)),
                       ("今年", "{0}年".format(now.year)),
                       ("这个月", "{0}年{1}月".format(now.year, now.month))]:
        keyword = keyword.replace(char, repl)

    keyword = keyword.split(r"．")[-1]
    keywords = keyword.split(" ")
    keyword = "".join([e.strip("\r\n") for e in keywords if e])
    return keyword

def convertjpg(jpgfile,outfile):
    img=Image.open(jpgfile)
    new_img=img.resize((int(1080/5),int(1920/5)),Image.BILINEAR)
    new_img.save(outfile)

def main():
    args = parse_args()
    timeout = args.timeout

    adb_bin = get_adb_tool()
    if use_monitor:
        os.system("{0} connect 127.0.0.1:62001".format(adb_bin))

    check_screenshot(filename="screenshot.png", directory=data_directory)

    # stdout_queue = Queue(10)
    # ## spaw baidu count
    # baidu_queue = Queue(5)
    # baidu_search_job = multiprocessing.Process(target=baidu_count_daemon,
    #                                            args=(baidu_queue, stdout_queue, timeout))
    # baidu_search_job.daemon = True
    # baidu_search_job.start()
    #
    # ## spaw crawler
    # knowledge_queue = Queue(5)
    # knowledge_craw_job = multiprocessing.Process(target=crawler_daemon,
    #                                              args=(knowledge_queue, stdout_queue))
    # knowledge_craw_job.daemon = True
    # knowledge_craw_job.start()
    #
    # ## output threading
    # output_job = threading.Thread(target=print_terminal, args=(stdout_queue,))
    # output_job.daemon = True
    # output_job.start()

    if enable_chrome:
        closer = Event()
        noticer = Event()
        noticer.clear()
        reader, writer = Pipe()
        browser_daemon = multiprocessing.Process(
            target=run_browser, args=(closer, noticer, reader,))
        browser_daemon.daemon = True
        browser_daemon.start()

    def __inner_job():
        start = time.time()
        analyze_current_screen_text(
            directory=data_directory,
            compress_level=image_compress_level[0],
            crop_area=crop_areas[game_type],
            use_monitor=use_monitor
        )
        #######################################################缩放 测试1920*1080
        text_area_file= os.path.join(data_directory, "text_area.png")
        text_area_file_scale = os.path.join(data_directory, "text_area_scale.png")
        convertjpg(text_area_file,text_area_file_scale)
        text_binary_scale=get_area_data(text_area_file_scale)
        start2 = time.time()
        ###########################################################
        keywords = get_text_from_image(
            image_data=text_binary_scale,
            timeout=timeout
        )
        end2 = time.time()
        print ("use2: %f" % (end2-start2))
        #####################################################
        if not keywords:
            print("text not recognize")
            return

        true_flag, real_question, question, answers = parse_question_and_answer(keywords)

        if game_type == "UC答题":
            answers = map(lambda a: a.rsplit(":")[-1], answers)

        print("~" * 60)
        print("{0}\n{1}".format(real_question, "\n".join(answers)))
        print("~" * 60)

        # ### refresh question
        # stdout_queue.put({
        #     "type": 0,
        #     "data": "{0}\n{1}".format(question, "\n".join(answers))
        # })
        #
        # # notice baidu and craw
        # baidu_queue.put((
        #     question, answers, true_flag
        # ))
        # knowledge_queue.put(question)

        if enable_chrome:
            writer.send(question)
            noticer.set()

        summary = baidu_count(question, answers, timeout=timeout)
        summary_li = sorted(summary.items(), key=operator.itemgetter(1), reverse=True)
        if true_flag:
            recommend = "{0}\n{1}".format(
                "肯定回答(**)： {0}".format(summary_li[0][0]),
                "否定回答(  )： {0}".format(summary_li[-1][0]))
        else:
            recommend = "{0}\n{1}".format(
                "肯定回答(  )： {0}".format(summary_li[0][0]),
                "否定回答(**)： {0}".format(summary_li[-1][0]))
        print("*" * 60)
        print("\n".join(map(lambda item: "{0}: {1}".format(item[0], item[1]), summary_li)))
        print(recommend)
        print("*" * 60)

        ans = kwquery(real_question)
        print("-" * 60)
        print(wrap(" ".join(ans), 60))
        print("-" * 60)

        end = time.time()
        # stdout_queue.put({
        #     "type": 3,
        #     "data": "use {0} 秒".format(end - start)
        # })
        print("use {0} 秒".format(end - start))
        save_screen(
            directory=data_directory
        )
        time.sleep(1)

    print("""
            请选择答题节目:
              1. 百万英雄
              2. 冲顶大会
              3. 芝士超人
              4. UC答题
            """)
    game_type = input("输入节目序号: ")
    if game_type == "1":
        game_type = '百万英雄'
    elif game_type == "2":
        game_type = '冲顶大会'
    elif game_type == "3":
        game_type = "芝士超人"
    elif game_type == "4":
        game_type = "UC答题"
    else:
        game_type = '百万英雄'

    while True:
        enter = input("按Enter键开始，按ESC键退出...")
        if enter == chr(27):
            break
        try:
            clear_screen()
            __inner_job()
        except Exception as e:
            import traceback

            traceback.print_exc()
            print(str(e))

    print("欢迎下次使用")
    if enable_chrome:
        reader.close()
        writer.close()
        closer.set()
        time.sleep(3)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()

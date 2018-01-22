# -*- coding:utf-8 -*-


"""

    Xi Gua video Million Heroes

"""
import logging.handlers
import multiprocessing
import os
import threading
import time
from argparse import ArgumentParser
from datetime import datetime
from functools import partial
from multiprocessing import Event, Pipe, Queue

from config import api_key, enable_chrome, use_monitor, image_compress_level, crop_areas
from config import api_version
from config import app_id
from config import app_key
from config import app_secret
from config import data_directory
from config import prefer
from core.android import save_screen, check_screenshot, get_adb_tool, analyze_current_screen_text
from core.check_words import parse_false
from core.chrome_search import run_browser
from core.crawler.crawl import jieba_initialize, crawler_daemon
from core.crawler.pmi import baidu_count_daemon
from core.ocr.baiduocr import get_text_from_image as bai_get_text
from core.ocr.spaceocr import get_text_from_image as ocrspace_get_text
from utils import stdout_template
from utils.backup import save_question_answers_to_file, get_qa_list, upload_to_cloud
from utils.process_stdout import ProcessStdout

logger = logging.getLogger("assistant")
handler = logging.handlers.WatchedFileHandler("assistant.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

## jieba init
jieba_initialize()

if prefer[0] == "baidu":
    get_text_from_image = partial(bai_get_text,
                                  app_id=app_id,
                                  app_key=app_key,
                                  app_secret=app_secret,
                                  api_version=api_version,
                                  timeout=5)

elif prefer[0] == "ocrspace":
    get_text_from_image = partial(ocrspace_get_text, api_key=api_key)


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


def sync_data_daemon(stdoutpipe):
    qa_li = get_qa_list("screenshots/QA.txt")
    ok = upload_to_cloud(qa_li)
    if ok:
        stdoutpipe.put("同步信息到云端成功")
    else:
        stdoutpipe.put("同步信息到云端错误")


def prompt_message():
    global game_type
    print("""
请选择答题节目:
    1. 百万英雄
    2. 冲顶大会
    3. 芝士超人
    4. UC答题
    5. 自适应
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
    elif game_type == "5":
        game_type = "自适应"
    else:
        game_type = '自适应'


def main():
    args = parse_args()
    timeout = args.timeout

    adb_bin = get_adb_tool()
    if use_monitor:
        os.system("{0} connect 127.0.0.1:62001".format(adb_bin))

    check_screenshot(filename="screenshot.png", directory=data_directory)

    std_pipe = ProcessStdout()
    ## start to sync qa to cloud
    sync_job = threading.Thread(target=sync_data_daemon, args=(std_pipe.queue,))
    sync_job.daemon = True
    sync_job.start()

    ## spaw baidu count
    baidu_queue = Queue(5)
    baidu_search_job = multiprocessing.Process(target=baidu_count_daemon,
                                               args=(baidu_queue, std_pipe.queue, timeout))
    baidu_search_job.daemon = True
    baidu_search_job.start()

    ## spaw crawler
    knowledge_queue = Queue(5)
    knowledge_craw_job = multiprocessing.Process(target=crawler_daemon,
                                                 args=(knowledge_queue, std_pipe.queue))
    knowledge_craw_job.daemon = True
    knowledge_craw_job.start()

    ## output threading
    output_job = threading.Thread(target=std_pipe.run_forever)
    output_job.daemon = True
    output_job.start()

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
        image_binary = analyze_current_screen_text(
            directory=data_directory,
            compress_level=image_compress_level[0],
            crop_area=crop_areas[game_type]
        )
        if not image_binary:
            print("do not detect question and answers")
            return

        keywords = get_text_from_image(
            image_data=image_binary,
            timeout=timeout
        )
        if not keywords:
            print("text not recognize")
            return

        true_flag, real_question, question, answers = parse_question_and_answer(keywords)

        ### parse for answer
        answers = map(lambda a: a.rsplit(":")[-1], answers)
        answers = list(map(lambda a: a.rsplit(".")[-1], answers))

        std_pipe.write(stdout_template.QUESTION_TPL.format(real_question, "\n".join(answers)))

        # notice baidu and craw
        baidu_queue.put((
            question, answers, true_flag
        ))
        knowledge_queue.put(question)
        if enable_chrome:
            writer.send(question)
            noticer.set()

        end = time.time()
        std_pipe.write(stdout_template.TIME_CONSUME_TPL.format(end - start))
        save_screen(directory=data_directory)
        save_question_answers_to_file(real_question, answers, directory=data_directory)

    prompt_message()
    while True:
        enter = input("按Enter键开始，切换游戏请输入s，按ESC键退出...\n")
        if enter == chr(27):
            break
        if enter == 's':
            prompt_message()
        try:
            __inner_job()
        except Exception as e:
            logger.error(str(e), exc_info=True)

    print("欢迎下次使用")
    if enable_chrome:
        reader.close()
        writer.close()
        closer.set()
        time.sleep(3)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()

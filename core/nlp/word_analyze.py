# -*- coding: utf-8 -*-


import multiprocessing

import jieba
import jieba.analyse

jieba.enable_parallel(multiprocessing.cpu_count())

Noun_flags = [
    "n",
    "nr",
    "nr2",
    "nrj",
    "nrf",
    "ns"
    "nsf"
    "nt"
    "nz",
    "nl",
    "ng"
    "v",
    "vn",
    "an",

]


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


def analyze_keyword_from_question(question):
    """
    analyze the main key words from questions

    :param question:
    :return:
    """
    question = pre_process_question(question)
    main_keywords = jieba.analyse.extract_tags(
        question,
        topK=20,
        withWeight=False,
        allowPOS=Noun_flags
    )
    return " ".join(main_keywords)

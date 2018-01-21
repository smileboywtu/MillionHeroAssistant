# -*- coding: utf-8 -*-

"""

    Baidu zhidao searcher

"""
import logging
import operator
import random

import requests

from core.crawler import text_process as T
from utils import stdout_template

Agents = (
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.71 Safari/537.36"
)

logger = logging.getLogger("assistant")


def count_key_words(text, keywords):
    total_count = 0
    for keyword in keywords:
        total_count += text.count(keyword)
    return total_count


def get_rid_of_x(answers):
    """
    Get rid of x flag in answer
    
    :param answers: 
    :return: 
    """
    final = []
    for ans in answers:
        final.append("".join([ans.word for ans in T.postag(ans) if "x" not in ans.flag]))
    return final


def just_keep_none(answer):
    words = T.postag(answer)
    final_none = []
    for word in words:
        if "n" in word.flag or "a" in word.flag or "x" in word.flag or "q" in word.flag:
            final_none.append(word.word)
    if final_none:
        final_none.append(answer)
    return [answer] if not final_none else final_none


def sougou_count(keyword, answers, timeout=5):
    """
    count answer number in sougou response
    
    :param keyword: 
    :param answers: 
    :param timeout: 
    :return: 
    """
    headers = {
        "User-Agent": random.choice(Agents),
    }
    params = {
        "query": keyword,
    }
    resp = requests.get("https://www.sogou.com/web", params=params, headers=headers)
    if not resp.ok:
        logger.error("Get SouGou HTTP ERROR")
        return {
            ans: 0
            for ans in answers
        }
    summary = {
        ans: resp.text.count(ans)
        for ans in answers
    }
    if all([cnt == 0 for cnt in summary.values()]):
        answers = get_rid_of_x(answers)
        return {
            ans: resp.text.count(ans)
            for ans in answers
        }
    return summary


def baidu_count(keyword, answers, timeout=5):
    """
    Count the answer number from first page of baidu search

    :param keyword:
    :param timeout:
    :return:
    """
    headers = {
        "Host": "www.baidu.com",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": random.choice(Agents)
    }
    params = {
        "wd": keyword,
        "ie": "utf-8"
    }
    resp = requests.get("http://www.baidu.com/s", params=params, headers=headers)
    if not resp.ok:
        logger.error("Get BaiDu HTTP ERROR")
        return {
            ans: 0
            for ans in answers
        }

    # answers_li = list(map(just_keep_none, answers))
    # summary = {
    #     ans: count_key_words(resp.text, ans_li)
    #     for ans, ans_li in zip(answers, answers_li)
    # }
    summary = {
        ans: resp.text.count(ans)
        for ans in answers
    }
    if all([cnt == 0 for cnt in summary.values()]):
        answers = get_rid_of_x(answers)
        return {
            ans: resp.text.count(ans)
            for ans in answers
        }

    default = list(summary.values())[0]
    if all([value == default for value in summary.values()]):
        answer_firsts = {
            ans: resp.text.index(ans)
            for ans in answers
        }
        sorted_li = sorted(answer_firsts.items(), key=operator.itemgetter(1), reverse=False)
        answer_li, index_li = zip(*sorted_li)
        return {
            a: b
            for a, b in zip(answer_li, reversed(index_li))
        }
    return summary


def baidu_count_daemon(exchage_queue, outputqueue, timeout=5):
    """
    count words
    
    :return: 
    """
    while True:
        question, answers, true_flag = exchage_queue.get()
        try:
            baidu_summary = baidu_count(question, answers, timeout=timeout)
            sougou_summary = sougou_count(question, answers, timeout=timeout)
            summary = {
                key: baidu_summary[key] + sougou_summary[key]
                for key in baidu_summary
            }
            summary_li = sorted(summary.items(), key=operator.itemgetter(1), reverse=True)
            if true_flag:
                recommend = "{0}\n{1}".format(
                    "肯定回答(**)： {0}".format(summary_li[0][0]),
                    "否定回答(  )： {0}".format(summary_li[-1][0]))
            else:
                recommend = "{0}\n{1}".format(
                    "肯定回答(  )： {0}".format(summary_li[0][0]),
                    "否定回答(**)： {0}".format(summary_li[-1][0]))
            outputqueue.put(stdout_template.BAIDU_TPL.format(
                "\n".join(map(lambda item: "{0}: {1}".format(item[0], item[1]), summary_li)),
                recommend
            ))
        except Exception as e:
            logger.error(str(e), exc_info=True)

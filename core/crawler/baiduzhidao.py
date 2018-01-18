# -*- coding: utf-8 -*-

"""

    Baidu zhidao searcher

"""
import operator
import random

import requests

from core.crawler import text_process as T

Agents = (
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
)


def baidu_count(keyword, answers, timeout=2):
    """
    Count the answer number from first page of baidu search

    :param keyword:
    :param timeout:
    :return:
    """
    headers = {
        # "Cache-Control": "no-cache",
        "Host": "www.baidu.com",
        "User-Agent": random.choice(Agents)
    }
    params = {
        "wd": keyword.encode("gbk")
    }
    resp = requests.get("http://www.baidu.com/s", params=params, headers=headers, timeout=timeout)
    if not resp.ok:
        print("baidu search error")
        return {
            ans: 0
            for ans in answers
        }
    summary = {
        ans: resp.text.count(ans)
        for ans in answers
    }

    if all([cnt == 0 for cnt in summary.values()]):
        return summary

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


def baidu_count_daemon(exchage_queue, outputqueue, timeout=3):
    """
    count words
    
    :return: 
    """

    def just_keep_none(answer):
        words = T.postag(answer)
        final_none = []
        for word in words:
            if "n" in word.flag:
                final_none.append(word.word)
        return answer if not final_none else " ".join(final_none)

    while True:
        question, answers, true_flag = exchage_queue.get()
        try:
            answers = map(just_keep_none, answers)
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
            outputqueue.put({
                "type": 1,
                "data": "{0}\n{1}".format(
                    "\n".join(map(lambda item: "{0}: {1}".format(item[0], item[1]), summary_li)),
                    recommend
                )
            })
        except:
            import traceback
            traceback.print_exc()

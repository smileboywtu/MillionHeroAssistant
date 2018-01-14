# -*- coding: utf-8 -*-

"""

    Baidu zhidao searcher

"""
import operator

import random
import requests

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

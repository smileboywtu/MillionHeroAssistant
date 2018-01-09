# -*- coding: utf-8 -*-


import requests
from lxml import html


def get_general_number(result):
    for item in ("About", ",", "results"):
        result = result.replace(item, "")
    return result


def search_result_number(keyword, timeout=2):
    """
    Search keyword and get search number

    :param keyword:
    :param timeout:
    :return:
    """
    url = "http://www.baidu.com/s"
    params = {
        "q": keyword
    }
    resp = requests.get(url, params=params, timeout=timeout)
    if not resp.ok:
        print("google search error")
        return 0
    parser = html.fromstring(resp.text)
    result = parser.xpath("//div[@id='resultStats']/text()")
    if not result:
        return 0

    return int(get_general_number(result[0]))

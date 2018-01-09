# -*- coding: utf-8 -*-

"""

    Baidu zhidao searcher

"""

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

import requests
from lxml import html


def zhidao_search(keyword, default_answer_select, timeout=2):
    """
    Search BaiDu zhidao net

    :param keyword:
    :param timeout:
    :return:
    """
    answer_url_li = parse_search(
        keyword=keyword,
        default_answer_select=default_answer_select,
        timeout=timeout)
    return parse_answer(answer_url_li)


def parse_search(keyword, default_answer_select=2, timeout=2):
    """
    Parse BaiDu zhidao search

    only return the first `default_answer_select`

    :param keyword:
    :param default_answer_select:
    :return:
    """
    params = {
        "lm": "0",
        "rn": "10",
        "pn": "0",
        "fr": "search",
        "ie": "gbk",
        "word": keyword.encode("gbk")
    }

    url = "https://zhidao.baidu.com/search"
    resp = requests.get(url, params=params, timeout=timeout)
    if not resp.ok:
        print("baidu zhidao api error")
        return ""
    parser = html.fromstring(resp.text)
    question_li = parser.xpath("//*[@id='page-main']//div[@class='list-inner']/*[@id='wgt-list']/dl/dt/a/@href")
    return question_li[:default_answer_select]


def parse_answer(urls, timeout=2):
    def fetch(url):
        resp = requests.get(url, timeout=timeout)
        if not resp.ok:
            return ""
        if resp.encoding == "ISO-8859-1" or not resp.encoding:
            resp.encoding = requests.utils.get_encodings_from_content(resp.text)[0]
        return resp.text

    final = []
    with ThreadPoolExecutor(5) as executor:
        future_to_url = {
            executor.submit(fetch, url): url
            for url in urls
        }

        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                text = future.result()
                parser = html.fromstring(text)
                parts = parser.xpath(
                    "//*[contains(@id, 'best-answer')]//*[@class='line content']/*[contains(@id, 'best-content')]/text()")
                if not parts:
                    parts = parser.xpath(
                        "//*[@id='wgt-answers']//*[contains(@class, 'answer-first')]//*[contains(@id, 'answer-content')]//span[@class='con']/text()")
                final.append(" ".join(parts))
            except Exception as exc:
                print("get url: {0} error: {1}".format(url, str(exc)))

    return final

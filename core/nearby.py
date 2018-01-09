# -*- coding: utf-8 -*-

"""

    calculate question and answer relation

    k = count(Q&A) / (count(Q) * count(A))

"""
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

import operator
from functools import partial

from core.baiduzhidao import search_result_number


def current_fetch(keywords_li):
    results = {}
    with ThreadPoolExecutor(10) as executor:
        future_to_url = {
            executor.submit(search_result_number, keyword): i
            for i, keyword in enumerate(keywords_li)
        }

        for future in as_completed(future_to_url):
            index = future_to_url[future]
            try:
                results[index] = future.result()
            except Exception as exc:
                print("get result number of question failed: {0}".format(str(exc)))
    results = sorted(results.items(), key=operator.itemgetter(0))
    return [item[1] for item in results]


def k_value(rela_count, answer_count, question_count):
    """
        k = count(Q&A) / (count(Q) * count(A))

    :param rela_count:
    :param answer_count:
    :param question_count:
    :return:
    """
    if answer_count == 0:
        return 0

    return rela_count / (answer_count * question_count)


def calculate_relation(question, answers):
    """

    :param question:
    :param answers:
    :return:
    """
    keywords_li = []
    keywords_li.extend(answers)
    keywords_li.extend([question + " " + item for item in answers])

    results = current_fetch(keywords_li)
    answ_len = len(answers)
    answer_frequency = results[:answ_len]
    combine_frequency = results[answ_len:]

    weight = partial(k_value, question_count=1)
    weight_li = [weight(rela, single) for rela, single in zip(combine_frequency, answer_frequency)]
    final = sorted(weight_li, reverse=True)[0]
    index = weight_li.index(final)
    return weight_li, final, index

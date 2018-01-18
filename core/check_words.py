# -*- coding: utf-8 -*-


FALSE = (
    "是错",
    "没有",
    "不属于",
    "不是",
    "不能",
    "不可以",
    "不对",
    "不正确",
    "不提供",
    "不包括",
    "不存在",
    "不经过",
    "未",
    "错误"
)


def parse_false(question):
    """

    :param question:
    :return:
    """
    for item in FALSE:
        if item in question:
            question = question.replace(item, "")
            return question, False

    return question, True

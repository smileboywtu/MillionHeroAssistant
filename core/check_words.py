# -*- coding: utf-8 -*-



FALSE = (
    "不",
    "是错"
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

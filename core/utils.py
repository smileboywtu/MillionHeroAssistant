# -*- coding: utf-8 -*-
import os


def save_question_answers_to_file(question, answers, directory=".", filename="QA.txt"):
    """
    bake the question and answers

    :param directory:
    :param filename:
    :return:
    """
    with open(os.path.join(directory, filename), "at") as baker:
        baker.write(";".join([question, ",".join(answers)]) + "\n")


def number_normalize(number, max_member, min_member, c=100):
    """
    Calculate normalize number

    :param number:
    :param max_member:
    :param min_member:
    :return:
    """
    if max_member == min_member:
        return number
    return (number - min_member) * c / (max_member - min_member)

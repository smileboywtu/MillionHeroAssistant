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

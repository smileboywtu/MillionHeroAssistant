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


def get_qa_list(source_file):
    """
    upload all question and answer to cloud
    
    :param period: 
    :return: 
    """
    try:
        fp = open("screenshots/QA.txt", "rt")
        qa_li = {}
        for line in fp.readlines():
            line = line.strip()
            if not line:
                continue
            pair = line.split(";")
            if len(pair) != 2:
                continue
            question, answers = pair[0], pair[1]
            answers = answers.split(",")
            qa_li[question] = answers
        return qa_li
    finally:
        fp.close()

# coding:utf8

import jieba.posseg as pseg

'''
initialize jieba Segment
'''


def postag(text):
    words = pseg.cut(text)
    return words
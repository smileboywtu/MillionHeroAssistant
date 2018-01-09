# -*- coding: utf-8 -*-

"""

    add text summary

"""

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.utils import get_stop_words

LANGUAGE = "chinese"
SENTENCES_COUNT = 5


def get_summary(long_text, sentences=SENTENCES_COUNT):
    parser = PlaintextParser.from_string(long_text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    return [str(sentence) for sentence in summarizer(parser.document, sentences)]

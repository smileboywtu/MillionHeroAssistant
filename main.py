# -*- coding:utf-8 -*-


"""

    Xi Gua video Million Heroes

"""
import textwrap
import time
from argparse import ArgumentParser

from config import data_directory, hanwan_appcode, summary_sentence_count
from config import default_answer_number
from config import text_summary
from core.android import analyze_current_screen_text
from core.baiduzhidao import zhidao_search
from core.hanwanocr import get_text_from_image
from core.textsummary import get_summary


def parse_args():
    parser = ArgumentParser(description="Million Hero Assistant")
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=5,
        help="default http request timeout"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    timeout = args.timeout

    start = time.time()
    text_binary = analyze_current_screen_text(
        directory=data_directory
    )
    keyword = get_text_from_image(
        image_data=text_binary,
        appcode=hanwan_appcode
    )
    if not keyword:
        print("text not recognize")
        return

    keyword = keyword.split(r"．")[-1]
    keywords = keyword.split(" ")
    keyword = "".join([e.strip("\r\n") for e in keywords if e])
    print("guess keyword: ", keyword)
    answers = zhidao_search(
        keyword=keyword,
        default_answer_select=default_answer_number,
        timeout=timeout
    )
    answers = filter(None, answers)

    for text in answers:
        print('=' * 70)
        text = text.replace("\u3000", "")
        if len(text) > 120 and text_summary:
            sentences = get_summary(text, summary_sentence_count)
            sentences = filter(None, sentences)
            if not sentences:
                print(text)
            else:
                print("\n".join(sentences))
        else:
            print("\n".join(textwrap.wrap(text, width=45)))

    end = time.time()
    print("use {0} 秒".format(end - start))


if __name__ == "__main__":
    main()

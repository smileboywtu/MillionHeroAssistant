import wda
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import textwrap
from functools import partial
from PIL import Image
from argparse import ArgumentParser

from config import app_id
from config import app_key
from config import app_secret
from config import data_directory
from config import default_answer_number
from config import hanwan_appcode
from config import image_compress_level
from config import prefer
from config import summary_sentence_count
from config import text_summary
from core.baiduzhidao import zhidao_search
from core.ocr.baiduocr import get_text_from_image as bai_get_text
from core.ocr.hanwanocr import get_text_from_image as han_get_text
from core.textsummary import get_summary


if prefer[0] == "baidu":
    get_text_from_image = partial(bai_get_text, app_id=app_id, app_key=app_key, app_secret=app_secret, timeout=5)
elif prefer[0] == "hanwang":
    get_text_from_image = partial(han_get_text, appcode=hanwan_appcode, timeout=3)

c = wda.Client()
s = c.session()

    
# def analyze_current_screen_text():
#     c.screenshot('screenshot.png')
#     img = np.array(Image.open('autojump.png'))
#     wide = img.size[0]
#     img = img.crop((70, 200, wide - 70, 700))


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

    c.screenshot('screenshot.png')
    img = Image.open('screenshot.png')
    wide = img.size[0]
    img1 = img.crop((70, 200, wide - 70, 800))
    img1.save('screenshot.png')
    text_binary = open('screenshot.png','rb').read()

    keyword = get_text_from_image(
        image_data=text_binary,
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

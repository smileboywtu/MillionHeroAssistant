import wda
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import textwrap
import time
from PIL import Image
from argparse import ArgumentParser
from config import data_directory, hanwan_appcode
from config import default_answer_number
from core.baiduzhidao import zhidao_search
from core.hanwanocr import get_text_from_image

import urllib.request, sys,base64,json,os,time,pyperclip,baiduSearch

c = wda.Client()
s = c.session()

    
def analyze_current_screen_text():
    c.screenshot('screenshot.png')
    img = np.array(Image.open('autojump.png'))
    wide = img.size[0]
    img = img.crop((70, 200, wide - 70, 700))


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
        appcode=hanwan_appcode
    )
    if not keyword:
        print("text not recognize")
        return

    keyword = keyword.split(r"．")[-1]
    keywords = keyword.split(" ")
    keyword = "".join([e.strip("\r\n") for e in keywords if e])
    print("主人,您的问题可能是 : ", keyword)
    answers = zhidao_search(
        keyword=keyword,
        default_answer_select=default_answer_number,
        timeout=timeout
    )
    answers = filter(None, answers)
    for ans in answers:
        print('='*70)
        ans = ans.replace("\u3000", "")
        ans = ans[0:400]
        print("\n".join(textwrap.wrap(ans, width=45)))
    end = time.time()
    print("use {0} 秒".format(end - start))



## 百度搜索
# def main():
#     args = parse_args()
#     timeout = args.timeout

#     start = time.time()

#     c.screenshot('screenshot.png')
#     img = Image.open('screenshot.png')
#     wide = img.size[0]
#     img1 = img.crop((70, 200, wide - 70, 730))
#     img1.save('screenshot.png')
#     text_binary = open('screenshot.png','rb').read()

#     keyword = get_text_from_image(
#         image_data=text_binary,
#         appcode=hanwan_appcode
#     )
#     if not keyword:
#         print("text not recognize")
#         return
#     keyword = keyword.split(r"．")[-1]
#     keywords = keyword.split(" ")
#     keyword = "".join([e.strip("\r\n") for e in keywords if e])
#     print("主人,您的问题可能是 : ", keyword)


#     results = baiduSearch.search(keyword, convey=False)
#     print("主人,您的答案可能是 : ", results)
#     count = 0
#     for result in results:
#         print('{0} {1} {2} {3} {4}'.format(result.index, result.title, result.abstract, result.show_url, result.url))  # 此处应有格式化输出
#         print('{0}'.format(result.abstract))  # 此处应有格式化输出
#         count=count+1
#         if(count == 6):
#             break
#         end = time.time()
#     print("use {0} 秒".format(end - start))


if __name__ == "__main__":
    main()

# fig = plt.figure()
# pull_screenshot()
# img = np.array(Image.open('question.png'))
# im = plt.imshow(img, animated=True)


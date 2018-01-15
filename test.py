# -*- coding: utf-8 -*-


import unittest
from unittest import TestCase


class OcrTestCase(TestCase):
    """unittest"""

    def test_baidu_ocr(self):
        """
        test baidu ocr

        :return:
        """
        from core.ocr.baiduocr import get_text_from_image

        print("test baidu ocr")
        app_id = "10661627"
        app_key = "h5xcL0m4TB8fiiFWoysn7uxt"
        app_secret = "HGA1cgXzz80douKQUpII7K77TYWSGcfW"

        with open("screenshots/text_area.png", "rb") as fp:
            message = get_text_from_image(fp.read(), app_id, app_key, app_secret, 5)
            print(message)

    def test_detect_direction(self):
        """
        Test baidu api direction

        :return:
        """
        from core.ocr.baiduocr import get_text_from_image

        print("test baidu ocr direction")
        app_id = "10661627"
        app_key = "h5xcL0m4TB8fiiFWoysn7uxt"
        app_secret = "HGA1cgXzz80douKQUpII7K77TYWSGcfW"

        with open("screenshots/direction.png", "rb") as fp:
            message = get_text_from_image(fp.read(), app_id, app_key, app_secret, 5)
            print(message)

    def test_image_count(self):
        """

        :return:
        """
        from PIL import Image
        count_white = 0
        with Image.open("screenshots/screenshot.png") as img:
            w, h = img.size
            for pix in img.getdata():
                if all([i >= 240 for i in pix[:3]]):
                    count_white += 1

            print(count_white / (w * h))

    def test_crawler(self):
        """
        Test baidu crawler

        :return:
        """
        from core.crawler.crawl import kwquery
        from core.crawler.crawl import jieba_initialize
        jieba_initialize()
        query = "回锅肉属于哪一种菜系"
        ans = kwquery(query)
        print("~~~~~~~")
        for a in ans:
            print(a)
        print("~~~~~~~")

if __name__ == "__main__":
    unittest.main()

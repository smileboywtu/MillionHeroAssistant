# -*- coding: utf-8 -*-


import unittest
from unittest import TestCase

from core.baiduzhidao import search_result_number


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

    def test_search_result_number(self):
        print(search_result_number("唐朝"))


if __name__ == "__main__":
    unittest.main()

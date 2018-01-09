# -*- coding: utf-8 -*-


import unittest
from unittest import TestCase

from config import default_answer_number
from core.baiduzhidao import zhidao_search


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
            answers = zhidao_search(
                keyword=message,
                default_answer_select=default_answer_number,
                timeout=5
            )
            answers = filter(None, answers)
            print("".join(answers))

    # def test_hanwang_ocr(self):
    #     """
    #     test hanwang ocr
    #
    #     :return:
    #     """
    #     from core.ocr.hanwanocr import get_text_from_image
    #     print("test hanwang ocr")
    #     with open("screenshots/text_area2.png", "rb") as fp:
    #         print(get_text_from_image(fp.read(), appcode=""))



if __name__ == "__main__":
    unittest.main()

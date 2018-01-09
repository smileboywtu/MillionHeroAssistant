# -*- coding: utf-8 -*-


from unittest import TestCase

from core.ocr.baiduocr import get_text_from_image


class OcrTestCase(TestCase):
    """unittest"""

    def test_baidu_ocr(self):
        """
        test baidu ocr

        :return:
        """
        app_id = "10661627"
        app_key = "h5xcL0m4TB8fiiFWoysn7uxt"
        app_secret = "HGA1cgXzz80douKQUpII7K77TYWSGcfW"

        with open("screenshots/text_area.png", "rb") as fp:
            print(get_text_from_image(fp.read(), app_id, app_key, app_secret, 5))

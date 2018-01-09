# -*- coding: utf-8 -*-

"""

    baidu ocr

"""

from aip import AipOcr


def get_text_from_image(image_data, app_id, app_key, app_secret, timeout=3):
    """
    Get image text use baidu ocr

    :param image_data:
    :param app_id:
    :param app_key:
    :param app_secret:
    :param timeout:
    :return:
    """
    client = AipOcr(appId=app_id, apiKey=app_key, secretKey=app_secret)
    client.setConnectionTimeoutInMillis(timeout * 1000)

    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"

    result = client.basicAccurate(image_data, options)
    if "error_code" in result:
        print("baidu api error: ", result["error_msg"])
        return ""
    return [words["words"] for words in result["words_result"]]

# -*- coding: utf-8 -*-

"""

    baidu ocr

"""

from aip import AipOcr


def get_text_from_image(image_data, app_id, app_key, app_secret, api_version=0, timeout=3):
    """
    Get image text use baidu ocr

    :param image_data:
    :param app_id:
    :param app_key:
    :param app_secret:
    :param api_version:
    :param timeout:
    :return:
    """
    client = AipOcr(appId=app_id, apiKey=app_key, secretKey=app_secret)
    client.setConnectionTimeoutInMillis(timeout * 1000)

    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"

    if api_version == 1:
        result = client.basicAccurate(image_data, options)
    else:
        result = client.basicGeneral(image_data, options)

    if "error_code" in result:
        print("baidu api error: ", result["error_msg"])
        return ""
    return [words["words"] for words in result["words_result"]]

# -*- coding: utf-8 -*-
import json

import requests

"""

    ocr.space

"""


def get_text_from_image(image_data, api_key='6c851da45688957', overlay=False, language='chs'):
    """
    CR.space API request with local file.
    :param image_data: image's base64 encoding.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """
    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
    }
    r = requests.post('https://api.ocr.space/parse/image',
                      files={'image.png': image_data},
                      data=payload,
                      )
    result = json.loads(r.content)
    if (result['OCRExitCode'] == 1):
        return result['ParsedResults'][0]['ParsedText']
    print(result['ErrorMessage'])
    return ""

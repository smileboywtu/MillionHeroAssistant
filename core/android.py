# -*- coding: utf-8 -*-

"""

    use adb to capture the phone screen
    then use hanwang text recognize the text
    then use baidu to search answer

"""

from datetime import datetime

import os
from PIL import Image
from shutil import copyfile

from config import screen_corp_mode

def analyze_current_screen_text(directory=".", compress_level=1):
    """
    capture the android screen now

    :return:
    """
    print("capture time: ", datetime.now().strftime("%H:%M:%S"))
    screenshot_filename = "screenshot.png"
    save_text_area = os.path.join(directory, "text_area.png")
    capture_screen(screenshot_filename, directory)
    parse_answer_area(os.path.join(directory, screenshot_filename), save_text_area, compress_level)
    return get_area_data(save_text_area)


def analyze_stored_screen_text(screenshot_filename="screenshot.png", directory=".", compress_level=1):
    """
    reload screen from stored picture to store
    :param directory:
    :param compress_level:
    :return:
    """
    save_text_area = os.path.join(directory, "text_area.png")
    parse_answer_area(os.path.join(directory, screenshot_filename), save_text_area, compress_level)
    return get_area_data(save_text_area)


def capture_screen(filename="screenshot.png", directory="."):
    """
    use adb tools

    :param filename:
    :param directory:
    :return:
    """
    os.system("adb shell screencap -p /sdcard/{0}".format(filename))
    os.system("adb pull /sdcard/{0} {1}".format(filename, os.path.join(directory, filename)))


def save_screen(filename="screenshot.png", directory="."):
    """
    Save screen for further test
    :param filename:
    :param directory:
    :return:
    """
    copyfile(os.path.join(directory, filename),
             os.path.join(directory, datetime.now().strftime("%m%d_%H%M%S").join(os.path.splitext(filename))))


def parse_answer_area(source_file, text_area_file, compress_level):
    """
    crop the answer area

    :return:
    """

    image = Image.open(source_file)
    if compress_level == 1:
        image = image.convert("L")
    elif compress_level == 2:
        image = image.convert("1")
    wide = image.size[0]
    print("screen width: {0}, screen height: {1}".format(image.size[0], image.size[1]))

    if screen_corp_mode == "cd":
        ## 冲顶
        region = image.crop((120, 290, wide - 120, 1040))     
    else:
        ## 百万
        region = image.crop((70, 210, wide - 70, 1300))
        
    region.save(text_area_file)


def get_area_data(text_area_file):
    """

    :param text_area_file:
    :return:
    """
    with open(text_area_file, "rb") as fp:
        image_data = fp.read()
        return image_data
    return ""

# -*- coding: utf-8 -*-

"""

    use adb to capture the phone screen
    then use hanwang text recognize the text
    then use baidu to search answer

"""

import os
import platform
import subprocess
import sys
from datetime import datetime
from shutil import copyfile

import numpy as np
from PIL import Image
from skimage import morphology
from config import enable_scale

# SCREENSHOT_WAY 是截图方法，
# 经过 check_screenshot 后，会自动递
# 不需手动修改
SCREENSHOT_WAY = 3


def get_adb_tool():
    system_version = platform.system().upper()
    adb_bin = ""
    parent = "adb"
    if system_version.startswith("LINUX"):
        adb_bin = os.path.join(parent, "linux", "adb")
    if system_version.startswith("WINDOWS"):
        adb_bin = os.path.join(parent, "win", "adb.exe")
    if system_version.startswith("DARWIN"):
        adb_bin = os.path.join(parent, "mac", "adb")
    return adb_bin


def check_screenshot(filename, directory):
    """
    检查获取截图的方式
    """
    save_shot_filename = os.path.join(directory, filename)
    global SCREENSHOT_WAY
    if os.path.isfile(save_shot_filename):
        try:
            os.remove(save_shot_filename)
        except Exception:
            pass
    if SCREENSHOT_WAY < 0:
        print("暂不支持当前设备")
        sys.exit()
    capture_screen(filename, directory)
    try:
        Image.open(save_shot_filename).load()
        print("采用方式 {} 获取截图".format(SCREENSHOT_WAY))
    except Exception:
        SCREENSHOT_WAY -= 1
        check_screenshot(filename=filename, directory=directory)


def analyze_current_screen_text(crop_area, directory=".", compress_level=1):
    """
    capture the android screen now

    :return:
    """
    screenshot_filename = "screenshot.png"
    save_text_area = os.path.join(directory, "text_area.png")
    capture_screen_v2(screenshot_filename, directory)
    ok = parse_answer_area(os.path.join(directory, screenshot_filename),
                           save_text_area, compress_level, crop_area)
    return get_area_data(save_text_area) if ok else None


def capture_screen_v2(filename="screenshot.png", directory="."):
    """
    can't use general fast way

    :param filename:
    :param directory:
    :return:
    """
    adb_bin = get_adb_tool()
    os.system("{0} shell screencap -p /sdcard/{1}".format(adb_bin, filename))
    os.system("{0} pull /sdcard/{1} {2}".format(adb_bin, filename, os.path.join(directory, filename)))


def capture_screen(filename="screenshot.png", directory="."):
    """
    获取屏幕截图，目前有 0 1 2 3 四种方法，未来添加新的平台监测方法时，
    可根据效率及适用性由高到低排序

    :param filename:
    :param directory:
    :return:
    """
    global SCREENSHOT_WAY
    adb_bin = get_adb_tool()
    if 1 <= SCREENSHOT_WAY <= 3:
        process = subprocess.Popen(
            "{0} shell screencap -p".format(adb_bin),
            shell=True, stdout=subprocess.PIPE)
        binary_screenshot = process.stdout.read()
        if SCREENSHOT_WAY == 2:
            binary_screenshot = binary_screenshot.replace(b"\r\n", b"\n")
        elif SCREENSHOT_WAY == 1:
            binary_screenshot = binary_screenshot.replace(b"\r\r\n", b"\n")
        with open(os.path.join(directory, filename), "wb") as writer:
            writer.write(binary_screenshot)
    elif SCREENSHOT_WAY == 0:
        os.system("{0} shell screencap -p /sdcard/{1}".format(adb_bin, filename))
        os.system("{0} pull /sdcard/{1} {2}".format(adb_bin, filename, os.path.join(directory, filename)))


def save_screen(filename="screenshot.png", directory="."):
    """
    Save screen for further test
    :param filename:
    :param directory:
    :return:
    """
    copyfile(os.path.join(directory, filename),
             os.path.join(directory, datetime.now().strftime("%m%d_%H%M%S").join(os.path.splitext(filename))))


def auto_find_crop_area(source_file):
    """
    1. convert to gray picture
    2. find pixel > 200 (white) and connect
    3. if > image/4 
    4. find edge of question and answer
    
    :param source_file:
    :return: 
    """
    image = Image.open(source_file)
    width, height = image.size[0], image.size[1]
    array_img = np.array(image)
    ot_img = (array_img > 200)
    obj_dtec_img = morphology.remove_small_objects(ot_img, min_size=width * height / 4, connectivity=1)
    if np.sum(obj_dtec_img) < 1000:
        return []
    return [
        np.where(obj_dtec_img * 1.0 > 0)[1].min() + 20,
        np.where(obj_dtec_img * 1.0 > 0)[0].min(),
        np.where(obj_dtec_img * 1.0 > 0)[1].max(),
        np.where(obj_dtec_img * 1.0 > 0)[0].max()]


def parse_answer_area(source_file, text_area_file, compress_level, crop_area):
    """
    crop the answer area

    :return:
    """

    image = Image.open(source_file)
    width, height = image.size[0], image.size[1]

    if not crop_area:
        image = image.convert("L")
        array_img = np.array(image)
        ot_img = (array_img > 225)
        obj_dtec_img = morphology.remove_small_objects(ot_img, min_size=width * height / 4, connectivity=1)
        if np.sum(obj_dtec_img) < 1000:
            return False
        region = image.crop((
            np.where(obj_dtec_img * 1.0 > 0)[1].min() + 20,
            np.where(obj_dtec_img * 1.0 > 0)[0].min() + 215,
            np.where(obj_dtec_img * 1.0 > 0)[1].max(),
            np.where(obj_dtec_img * 1.0 > 0)[0].max()))
    else:
        if compress_level == 1:
            image = image.convert("L")
        elif compress_level == 2:
            image = image.convert("1")
        region = image.crop((width * crop_area[0], height * crop_area[1], width * crop_area[2], height * crop_area[3]))

    if enable_scale:
        region = region.resize((int(1080 / 3), int(1920 / 5)), Image.BILINEAR)
    region.save(text_area_file)
    return True


def get_area_data(text_area_file):
    """

    :param text_area_file:
    :return:
    """
    with open(text_area_file, "rb") as fp:
        image_data = fp.read()
        return image_data
    return ""

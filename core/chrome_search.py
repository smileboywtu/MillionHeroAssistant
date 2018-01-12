# -*- coding: utf-8 -*-

import platform
import time

import keyboard
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def browser_init():
    """
    Initialize browser

    :return:
    """
    system_version = platform.system().upper()
    browser_bin = ""
    parent = os.path.dirname(os.path.abspath(__file__))
    if system_version.startswith("LINUX"):
        browser_bin = os.path.join(parent, "drivers", "chromedriver-linux")
    if system_version.startswith("WINDOWS"):
        browser_bin = os.path.join(parent, "drivers", "chromedriver.exe")
    if system_version.startswith("MAC"):
        browser_bin = os.path.join(parent, "drivers", "chromedriver-mac")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--enable-automation")
    browser = webdriver.Chrome(browser_bin, chrome_options=chrome_options)
    browser.get("http://www.baidu.com")
    return browser


def run_browser(question_object):
    """
    run as a daemon

    :return:
    """
    try:

        browser = browser_init()
        print("浏览器加载成功")
    except Exception as e:
        print("浏览器加载失败")
        print(str(e))
    else:
        def key_press_callback(e):
            if keyboard.is_pressed("space"):
                browser_search(browser, question_object.value.decode("utf-8").encode("gbk"))

        keyboard.hook(key_press_callback)
        while True:
            time.sleep(2)
            keyboard.wait()


def browser_search(browser, questions):
    """
    search the browser

    :param browser:
    :param questions:
    :return:
    """
    elem = browser.find_element_by_id("kw")
    elem.clear()
    elem.send_keys(questions)
    elem.send_keys(Keys.RETURN)

# -*- coding: utf-8 -*-

import os
import platform

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def browser_init():
    """
    Initialize browser

    :return:
    """
    system_version = platform.system().upper()
    browser_bin = ""
    parent = "drivers"
    if system_version.startswith("LINUX"):
        browser_bin = os.path.join(parent, "chromedriver-linux")
    if system_version.startswith("WINDOWS"):
        browser_bin = os.path.join(parent, "chromedriver.exe")
    if system_version.startswith("DARWIN"):
        browser_bin = os.path.join(parent, "chromedriver-mac")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--enable-automation")
    browser = webdriver.Chrome(browser_bin, chrome_options=chrome_options)
    browser.get("http://www.baidu.com")
    return browser


def run_browser(closer, noticer, keyword_exchange):
    """
    run as a daemon

    :return:
    """
    try:

        browser = browser_init()
        print("\n浏览器加载成功")
    except Exception as e:
        print("\n浏览器加载失败")
        print(str(e))
    else:
        while True:
            if closer.is_set():
                browser.quit()

            noticer.wait(timeout=1)
            if noticer.is_set():
                question = keyword_exchange.recv()
                browser_search(browser, question)
                noticer.clear()
    finally:
        browser.quit()


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

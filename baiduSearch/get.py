import requests

__url = 'http://www.baidu.com/s?wd='  # 搜索请求网址


def page(word):
    r = requests.get(__url + word)
    if r.status_code == 200:  # 请求错误（不是200）处理
        return r.text
    else:
        print(r.status_code)
        return False

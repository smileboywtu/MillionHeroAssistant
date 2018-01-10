import requests
from bs4 import BeautifulSoup


# 定义返回的result类
class Result(object):

    def __init__(self, r_index, r_title, r_abstract, show_url, r_url):  # id似乎占用了内部名称，那就用index来代替吧
        self.__index = r_index
        self.__title = r_title
        self.__abstract = r_abstract
        self.__show_url = show_url
        self.__url = r_url

    @property
    def index(self):
        return self.__index

    @property
    def title(self):
        return self.__title

    @property
    def abstract(self):
        return self.__abstract

    @property
    def show_url(self):
        return self.__show_url

    @property
    def url(self):
        return self.__url

    def convey_url(self):
        self.__url = url(self.__url)


def page(html):
    # 初始化
    soup = BeautifulSoup(html, 'lxml')
    results = []

    # 获取结果来源
    result_set = soup.find(id='content_left')  # 结果全显示在页面左边
    result_set = result_set.find_all('div', class_='c-container')  # 结果class固定，其余为硬广

    for i in range(len(result_set)):  # 因为要index所以就用range来
        result = result_set[i]  # 其实就是result_div

        t_and_u = __get_title_and_c_url(result)
        c_title = t_and_u[0]  # 这个c_title就是title了
        c_url = t_and_u[1]  # c_url是百度的url，需要转换
        c_abstract = __get_abstract(result)  # 同title
        c_show_url = __get_show_url(result)

        result = Result(i + 1, c_title, c_abstract, c_show_url, c_url)
        results.append(result)

    return results


def url(r_url):
    return requests.get(r_url).url


# 获取title和c_url，这俩货恰好可以一起
def __get_title_and_c_url(result_div):
    r_from = result_div.find('a')  # 先获取第一个<a>，r refers to result
    if not r_from:
        return [None, None]
    for em in r_from.find_all('em'):  # 移除title中的em标签
        em.unwrap()
    return [r_from.get_text(), r_from['href']]


# 获取abstract
def __get_abstract(result_div):
    if 'result-op' not in result_div['class']:  # 不是软广
        r_from = result_div.find(class_='c-abstract')
        if not r_from:
            return None
        for em in r_from.find_all('em'):  # 移除abstract中的em标签
            em.unwrap()
        return r_from.get_text()
    else:
        return '百度软广，当前代码版本不予摘要'  # 其实是因为太麻烦


# 获取show_url
def __get_show_url(result_div):
    show = result_div.find(class_='c-showurl')
    if not show or show == '<span class="c-showurl"> </span>':  # 有些软广class不一样
        show = result_div.find(class_='c-showurl-color')
    if not show:  # 要是还不一样。。
        return '此结果未能如期获取到show url，提交issue帮助我们做的更好'
    return show.get_text()[:-2]  # 去除末尾/

# coding:utf8
import logging
import multiprocessing
import operator
import platform
from textwrap import wrap
from urllib.parse import quote

import jieba

from core.crawler import html_tools as To
from core.crawler import text_process as T
from utils import stdout_template


def jieba_initialize():
    if not platform.system().upper().startswith("WINDOWS"):
        jieba.enable_parallel(multiprocessing.cpu_count())
    jieba.load_userdict('resources/QAattrdic.txt')
    jieba.initialize()


def kwquery(query):
    '''
    对百度、 sougou Bing 的搜索摘要进行答案的检索
    （需要加问句分类接口）
    '''
    # 分词 去停用词 抽取关键词
    keywords = []
    words = T.postag(query)
    for k in words:
        # 只保留名词
        if k.flag.__contains__("n") or k.flag.__contains__("a") or k.flag.__contains__("t"):
            keywords.append(k.word)
    answer = []
    text = ''
    # 找到答案就置1
    flag = 0

    # 抓取百度前10条的摘要
    soup_baidu = To.get_html_baidu('https://www.baidu.com/s?wd=' + quote(query))

    for i in range(1, 10):

        if not soup_baidu:
            break

        results = soup_baidu.find(id=i)
        if not results:
            break

        # 判断是否有mu,如果第一个是百度知识图谱的 就直接命中答案
        if 'mu' in results.attrs and i == 1:
            r = results.find(class_='op_exactqa_s_answer')
            if not r:
                pass
            else:
                answer.append(r.get_text().strip())
                flag = 1
                break

        # 古诗词判断
        if "mu" in results.attrs and i == 1:
            r = results.find(class_="op_exactqa_detail_s_answer")
            if not r:
                pass
            else:
                answer.append(r.get_text().strip())
                flag = 1
                break

        # 万年历 & 日期
        if "mu" in results.attrs and i == 1 and results.attrs['mu'].__contains__(
                'http://open.baidu.com/calendar'):
            r = results.find(class_="op-calendar-content")
            if not r:
                pass
            else:
                answer.append(r.get_text().strip().replace("\n", "").replace(" ", ""))
                flag = 1
                break

        if "tpl" in results.attrs and i == 1 and results.attrs['tpl'].__contains__('calendar_new'):
            r = results.attrs['fk'].replace("6018_", "")
            print(r)

            if not r:
                pass
            else:
                answer.append(r)
                flag = 1
                break

        # 计算器
        if "mu" in results.attrs and i == 1 and results.attrs['mu'].__contains__(
                'http://open.baidu.com/static/calculator/calculator.html'):
            r = results.find('div').find_all('td')[1].find_all('div')[1]
            if not r:
                pass
            else:
                answer.append(r.get_text().strip())
                flag = 1
                break

        # 百度知道答案
        if "mu" in results.attrs and i == 1:
            r = results.find(class_='op_best_answer_question_link')
            if r == None:
                pass
            else:
                url = r['href']
                zhidao_soup = To.get_html_zhidao(url)
                r = zhidao_soup.find(class_='bd answer').find('pre')
                if r == None:
                    r = zhidao_soup.find(class_='bd answer').find(class_='line content')

                answer.append(r.get_text())
                flag = 1
                break

        if results.find("h3"):
            # 百度知道
            if results.find("h3").find("a").get_text().__contains__(u"百度知道") and (i == 1 or i == 2):
                url = results.find("h3").find("a")['href']
                if not url:
                    continue
                else:
                    zhidao_soup = To.get_html_zhidao(url)
                    r = zhidao_soup.find(class_='bd answer')
                    if not r:
                        continue
                    else:
                        r = r.find('pre')
                        if not r:
                            r = zhidao_soup.find(class_='bd answer').find(class_='line content')
                    answer.append(r.get_text().strip())
                    flag = 1
                    break

            # 百度百科
            if results.find("h3").find("a").get_text().__contains__(u"百度百科") and (i == 1 or i == 2):
                url = results.find("h3").find("a")['href']
                if url == None:
                    continue
                else:
                    baike_soup = To.get_html_baike(url)
                    r = baike_soup.find(class_='lemma-summary')
                    if not r:
                        continue
                    else:
                        r = r.get_text().replace("\n", "").strip()
                    answer.append(r)
                    flag = 1
                    break
        text += results.get_text()

    if flag == 1:
        return answer

    # 获取搜狗的答案
    soup_sougou = To.get_html_sougo("https://www.sogou.com/web?query=" + quote(query))
    answer_elements = soup_sougou.find_all("div", class_="vrwrap")
    for element in answer_elements:
        for best in element.find_all("div", class_="str-text-info"):
            if best.find("i", "str-green-skin"):
                answer.append(best.span.get_text())
                flag = 1
                break

    if flag == 1:
        return answer

    # 获取bing的摘要
    soup_bing = To.get_html_bing('https://www.bing.com/search?q=' + quote(query))
    # 判断是否在Bing的知识图谱中
    bingbaike = soup_bing.find(class_="bm_box")

    if bingbaike and \
            bingbaike.find_all(class_="b_vList")[1] and \
            bingbaike.find_all(class_="b_vList")[1].find("li"):
        flag = 1
        answer.append(bingbaike.get_text())
        return answer
    else:
        results = soup_bing.find(id="b_results")
        bing_list = results.find_all('li')
        for bl in bing_list:
            temp = bl.get_text()
            if temp.__contains__(u" - 必应网典"):
                url = bl.find("h2").find("a")['href']
                if url == None:
                    continue
                else:
                    bingwd_soup = To.get_html_bingwd(url)

                    r = bingwd_soup.find(class_='bk_card_desc').find("p")
                    if r == None:
                        continue
                    else:
                        r = r.get_text().replace("\n", "").strip()
                    answer.append(r)
                    flag = 1
                    break

        if flag == 1:
            return answer

        text += results.get_text()

    # 如果再两家搜索引擎的知识图谱中都没找到答案，那么就分析摘要
    if flag == 0:
        # 分句
        cutlist = [u"。", u"?", u".", u"_", u"-", u":", u"！", u"？"]
        temp = ''
        sentences = []
        for i in range(0, len(text)):
            if text[i] in cutlist:
                if temp == '':
                    continue
                else:
                    sentences.append(temp)
                temp = ''
            else:
                temp += text[i]

        # 找到含有关键词的句子,去除无关的句子
        key_sentences = {}
        for s in sentences:
            for k in keywords:
                if k in s:
                    key_sentences[s] = 1

        # 根据问题制定规则

        # 识别人名
        target_list = {}
        for ks in key_sentences:
            words = T.postag(ks)
            for w in words:
                if w.flag == ("nr"):
                    if w.word in target_list:
                        target_list[w.word] += 1
                    else:
                        target_list[w.word] = 1

        # 找出最大词频
        sorted_lists = sorted(target_list.items(), key=operator.itemgetter(1), reverse=True)
        sorted_lists2 = []
        for i, st in enumerate(sorted_lists):
            if st[0] in keywords:
                continue
            else:
                sorted_lists2.append(st)

        # print("返回前n个词频")
        answer = []
        for i, st in enumerate(sorted_lists2):
            if i < 3:
                answer.append(st[0])

    return answer


def crawler_daemon(keyword_queue, outputqueue):
    """
    Run as a daemon to crawl the web

    :param notice:
    :param reader:
    :return:
    """
    logger = logging.getLogger("assistant")
    while True:
        question = keyword_queue.get()
        try:
            ans = kwquery(question)
            outputqueue.put(stdout_template.KNOWLEDGE_TPL.format("\n".join(wrap("\n".join(ans), 45))))
        except Exception as e:
            logger.error(str(e), exc_info=True)


if __name__ == '__main__':
    query = "手机中常用的GPS定位用到了下列那项物理学成果"
    ans = kwquery(query)
    print("~~~~~~~")
    for a in ans:
        print(a)
    print("~~~~~~~")

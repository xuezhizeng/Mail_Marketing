#_*_encoding:utf-8_*_
"""
@Python -V: 3.X 
@SoftWave: Pycharm
@OS: Win10
@Author: SKYNE
@Contact: 520@skyne.cn
@Time: 2018.3.8
"""

import requests

from lxml import html

import random


def parser(url):
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.8", "Cache-Control": "max-age=0",
        "Connection": "keep-alive", "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36", }
    """
    :param url: 需要解析页面的url地址
    :return: selector
    """
    response = requests.get (url=url, headers=headers, verify=True)
    if response.status_code == 200:
        selector = html.fromstring(response.text)
        return selector
    else:
        print ("request error, please check! @SKYNE")

def get_article(url):
    """
    :param
    url : 需要进行获取信息的url地址
    flag : 标志位，判断是否抓取成功
    article : 字典，存储各信息
    :return: news 正常返回news，错误返回 -1
    """
    article = {}
    flag = None
    try:
        article['article-url'] = url
        selector = parser(url)
        article['article-abstract'] = str(selector.xpath('//article[@class="article-content"]//p/text()'))[1:160:1].strip (
            "', '").replace("', '", '').replace('\\xa0', '') + "......"
        article['article-title'] = selector.xpath('/html/head/title/text()')[0]
        article['cover-url'] = selector.xpath('//article[@class="article-content"]//p/img/@src')[0]
        article['article-label'] = selector.xpath('//div[@class="article-tags"]/a/text()')[0]
    except Exception as e:
        print ("url=", url, e)
        flag = 1
    if flag == None:
        return article
    else:
        return None


def get_book_list():
    """
    :param
    url : 需要进行获取信息的url地址
    flag : 标志位，判断是否抓取成功
    """

    # sd 后面跟数字，最多为4
    base_url = "http://jingyu.in/index.php/category/sd/"

    selector = parser(base_url)

    temp = selector.xpath('//article[@class="excerpt"]/header/h2/a')

    url_title = []
    for i in temp:
        url_title.append([i.text , i.get('href')])

    result = random.sample(url_title, 5)

    return result



if __name__ == '__main__':
    # print(get_article(url="http://jingyu.in/index.php/archives/1072/"))

    print(get_book_list())
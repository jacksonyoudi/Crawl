# coding: utf8

from urllib import request, response

"""
专门用于获取网页的抓取器，这里使用urllib
抓取器抽离出来是为了做 反扒机制的，
如： 自定义headers、代理ip、爬取频率等..

我习惯使用requests,使用系统的库urllib

"""


def Fetch(url):
    """
    :param url:  需要抓取的网页url
    :return:  返回转换成url的文档
    """

    # 如果需要构造请求头和代理使用
    # req = request.Request('http://www.douban.com/')
    # req.add_header('User-Agent',
    #                'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')

    with request.urlopen(url=url) as f:
        if f.status == 200:
            return f.read().decode('utf-8')
        else:
            # 抛出异常，记录日志
            raise "1111"



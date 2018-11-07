# coding=utf-8

"""
这里主要是用于解析抓取的网页，提取需要数据和url，

"""

from bs4 import BeautifulSoup
from engine.type import FidelityModel
from lib.tool import cov_date_format
from config import settings
from urllib import parse
from fetcher import Fetch
import traceback
from engine.type import Request
import datetime


from threading import Lock
target_format = "%Y-%m-%d"
source_format = "%m/%d/%Y"



mutex=Lock()
end_date = datetime.datetime.now() + datetime.timedelta(days=settings.days)


def _puase_date(link):
    """
    :param link:
      https://eresearch.fidelity.com/eresearch/conferenceCalls.jhtml?tab=dividends&begindate=11/5/2018
      根据 link提取日期
    :return: bool
    """
    url = parse.parse_qs(link)
    if url and url.get("begindate"):
        date_str = url.get("begindate")[0]
        date_link = datetime.datetime.strptime(date_str, "%m/%d/%Y")
        if date_link > end_date:
            return False
        else:
            return True

    else:
        return False


def fidelityParse(url="", queue=None, result_queue=None, uniq_urls=None):
    """
    :param url: url
    queue： request的队列
    result_queue：解析后数据的队列
    """
    htmldoc = Fetch(url)
    soup = BeautifulSoup(htmldoc, "html.parser")

    # 获取其他日期的，以及下一周的
    date_list_links = soup.find("div", class_="date-list-links").find("ul").findAll("li")
    for links in date_list_links:
        if links.attrs.get("class", [0])[0] in ["firstitem", "selected"]:
            continue
        link = links.find("a").attrs.get("href")
        complete_link = parse.urljoin(settings.Fidelity_Domain, link)
        # print(complete_link)
        # mutex.acquire()
        if _puase_date(complete_link):
            if uniq_urls is not None and not uniq_urls.get(complete_link):
                uniq_urls[complete_link] = 1
                print(len(uniq_urls))
                queue.put(Request(url=complete_link, ParserFunc=fidelityParse))
        # mutex.release()

    trs = soup.find("table", class_="datatable-component").find("tbody").find_all("tr")
    for tr in trs:
        try:
            tds = tr.findAll("td")
            th = tr.find("th")
            company = ""
            website = ""
            if th:
                company = th.find("strong").text
                website_elem = th.find("a", href="#")
                # 会出现没有的情况
                if website_elem:
                    website = th.find("a", href="#").attrs.get("onclick").split(",'")[1].strip("')")
            symbol = tds[0].text.replace("\n", "").replace("\t", "")
            if len(tds) < 6:
                continue
            dividend = tds[1].text
            announcement_date = cov_date_format(tds[2].text, source_format, target_format)
            record_date = cov_date_format(tds[3].text, source_format, target_format)
            ex_date = cov_date_format(tds[4].text, source_format, target_format)
            pay_date = cov_date_format(tds[5].text, source_format, target_format)
            result_queue.put(
                FidelityModel(company, website, symbol, dividend, announcement_date, record_date, ex_date, pay_date)
            )
        except Exception:
            traceback.print_exc()
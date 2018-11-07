# coding=utf-8


class Request():
    """
    请求的任务、 url和解析的函数
    """
    def __init__(self, url, ParserFunc):
        self.url = url
        self.parser_func = ParserFunc


class FidelityModel():
    def __init__(self, company, website, symbol, dividend, announcement_date, record_date, ex_date, pay_date):
        self.company = company
        self.website = website
        self.symbol = symbol
        self.dividend = dividend
        self.announcement_date = announcement_date
        self.record_date = record_date
        self.ex_date = ex_date
        self.pay_date = pay_date



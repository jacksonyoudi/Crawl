# coding=utf-8

import datetime


"""
常用的工具函数和类
"""


def cov_date_format(date_str, source_format, target_format):
    """
    :param date_str:  10/25/2018 原格式日期字符串
    :param source_format:  类似 %Y-%m-%d %H:%M:%S
    :param target_format: 日期格式 %Y-%m-%d %H:%M:%S
    :return: 转换后的日期格式
    """
    datetime_val = datetime.datetime.strptime(date_str, source_format)
    return datetime_val.strftime(target_format)



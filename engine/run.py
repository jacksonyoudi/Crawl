# coding: utf-8

from config import settings
import queue
import threading
from pipeline.csv_export import csv_export


class RequestThread(threading.Thread):
    """从队列读取数据"""

    def __init__(self, queue, worktype):
        """
         :param queue:     队列
         :param worktype:  其他参数
        """
        threading.Thread.__init__(self)
        self._jobq = queue
        self._work_type = worktype

    def run(self):
        while True:
            # 获取队列数据
            data = self._jobq.get(block=True)
            print("get", data, " worktype ", self._work_type)


class WorkThread(threading.Thread):
    """线程队列"""

    def __init__(self, *queue, worktype=None, func=None, uniq_urls=None):
        """
         :param queue:     队列
         :param worktype:  其他参数
        """
        threading.Thread.__init__(self)
        self._jobq = queue
        self._work_type = worktype
        self._func = func
        self._uniq_urls = uniq_urls

    def run(self):
        while True:
            # 获取队列数据
            self._func(*self._jobq, uniq_urls=self._uniq_urls)
            print("woking_thread is ", self._work_type)


def requestWork(queue, result_queue, uniq_urls=None):
    request = queue.get(block=True)
    request.parser_func(request.url, queue, result_queue, uniq_urls=uniq_urls)


# 这里就不抽象了, 为了兼容
def ResultWorkon(queue, uniq_urls=None):
    csv_export(settings.CSV_EXPORT_FILE_NAME, settings.CSV_EXPORT_FILE_TITLE, queue)


class Engine():
    def __init__(self, request):
        self.request = request
        self.Request_Q = queue.Queue()  # url队列
        self.Result_Q = queue.Queue()  # 结果队列
        self.urls = dict()  # 用于去重

    def run(self):
        # 第一个放入队列中
        self.Request_Q.put(self.request)

        # 请求处理的线程
        for i in range(settings.NUM_WORKERS):
            WorkThread(self.Request_Q, self.Result_Q, worktype=i, func=requestWork, uniq_urls=self.urls).start()

        # 导出的线程，考虑到导出csv有竞争问题，就一个线程
        WorkThread(self.Result_Q, worktype=0, func=ResultWorkon).start()
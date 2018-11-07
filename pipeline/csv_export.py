# coding=utf-8
import os
from config import settings
import datetime
import csv


def csv_export(name, title, queue):
    # 目录名
    file_dir = os.path.join(settings.basepath, "export/")
    if not os.path.exists(file_dir):
        os.makedirs(file_dir, 777)

    file_name = os.path.join(file_dir, "{}.csv".format(name))
    if os.path.exists(file_name):
        file_name_bak = os.path.join(file_dir,
                                     "{}_{}.csv".format(name, datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
        os.rename(file_name, file_name_bak)

    with open(file_name, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(title)

        while True:
            result = queue.get(block=True)
            result_list = [getattr(result, i, "") for i in title]
            print(result_list)
            spamwriter.writerow(result_list)

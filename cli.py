# coding=utf-8

import csv
from config.settings import basepath, CSV_EXPORT_FILE_NAME
import os
import datetime

import argparse
parser = argparse.ArgumentParser("search Fidelity Csv File")
parser.add_argument("-symbol", help="search by synbol")
parser.add_argument("-company", help="search by company")
parser.add_argument("-exdatestart", help="search by company")
parser.add_argument("-exdateend", help="search by company")



if __name__ == '__main__':
    args = parser.parse_args()
    if not args:
        print("please use -h")
    else:
        symbol = args.symbol
        company = args.company
        exdatestart = args.exdatestart
        exdateend = args.exdateend

        file_dir = os.path.join(basepath, "export/")
        file_name = os.path.join(file_dir, "{}.csv".format(CSV_EXPORT_FILE_NAME))
        if not os.path.exists(file_name):
            print("sorry, not csv file!!!!")
            exit(1)

        with open(file_name) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # symal
                if symbol and symbol != row.get("symbol"):
                    continue

                # company
                if company and company not in row.get("company"):
                    continue

                # date
                if exdatestart and exdateend:
                    date_start = datetime.datetime.strptime(exdatestart, "%Y-%m-%d")
                    date_end = datetime.datetime.strptime(exdateend, "%Y-%m-%d")
                    exdate = datetime.datetime.strptime(row.get("ex_date"), "%Y-%m-%d")
                    if exdate < date_start or exdate > date_end:
                        continue
                print(dict(row))










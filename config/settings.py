# coding=utf-8
import os

Fidelity_Domain = "https://eresearch.fidelity.com"

NUM_WORKERS = 3

basepath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

CSV_EXPORT_FILE_NAME = "fidelity"
CSV_EXPORT_FILE_TITLE = ["company", "website", "symbol", "dividend", "announcement_date", "record_date", "ex_date", "pay_date"]

days = 30
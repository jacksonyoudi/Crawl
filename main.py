# coding=utf-8
from engine.run import Engine
from engine.type import Request
from parser.fidelity import fidelityParse


if __name__ == '__main__':
    url = "https://eresearch.fidelity.com/eresearch/conferenceCalls.jhtml?tab=dividends"
    engine = Engine(Request(url=url, ParserFunc=fidelityParse))
    engine.run()

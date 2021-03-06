#!/usr/bin/python3.6
# -*- coding:utf-8 -*-

import schedule
import time
from subprocess import Popen
import logging
import threading
from biliob_analyzer.video_rank import computeVideoRank


def videoRank():
    computeVideoRank()


def site():
    Popen(["scrapy", "crawl", "site"])


def bangumi():
    Popen(["scrapy", "crawl", "bangumi"])


def donghua():
    Popen(["scrapy", "crawl", "donghua"])


def update_author():
    Popen(["scrapy", "crawl", "authorUpdate"])


def auto_add_author():
    Popen(["scrapy", "crawl", "authorAutoAdd"])


def video_watcher():
    Popen(["scrapy", "crawl", "videoWatcher"])


def video_spider():
    Popen(["scrapy", "crawl", "videoSpider"])


def video_spider_all():
    Popen(["scrapy", "crawl", "videoSpiderAll"])


def online():
    Popen(['scrapy', 'crawl', 'online'])


def strong():
    Popen(['scrapy', 'crawl', 'strong'])


def data_analyze():
    Popen(['python', 'run_analyzer.py'])


def weekly_analyze():
    Popen(['python', 'run_weekly_analyzer.py'])


def bili_monthly_rank():
    Popen(['scrapy', 'crawl', 'biliMonthlyRank'])


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


schedule.every().day.at('11:40').do(run_threaded, data_analyze)
schedule.every().day.at('01:00').do(run_threaded, update_author)
schedule.every().day.at('07:00').do(run_threaded, video_spider)
schedule.every().day.at('14:00').do(run_threaded, auto_add_author)
schedule.every().day.at('16:50').do(run_threaded, bangumi)
schedule.every().day.at('16:30').do(run_threaded, donghua)
schedule.every().day.at('22:00').do(run_threaded, video_watcher)
schedule.every().day.at('21:00').do(run_threaded, bili_monthly_rank)
schedule.every().week.do(run_threaded, video_spider_all)
schedule.every().week.do(run_threaded, videoRank)
schedule.every().hour.do(run_threaded, site)
schedule.every(15).minutes.do(run_threaded, online)
schedule.every(10).minutes.do(run_threaded, strong)


print('开始运行计划任务..')
while True:
    schedule.run_pending()
    time.sleep(60)

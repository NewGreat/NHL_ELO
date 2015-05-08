# -*- coding: utf-8 -*-

# Scrapy settings for results_scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os
import datetime as dt

today = dt.datetime.now()

BOT_NAME = 'results_scraper'

SPIDER_MODULES = ['results_scraper.spiders']
NEWSPIDER_MODULE = 'results_scraper.spiders'
LOG_FILE = 'logs/%s.log' % (today.strftime('%y.%m.%d %H:%M:%S'),)

DATABASE = {'drivername': 'postgres',
            'host': 'localhost',
            'port': '5432',
            'username': os.environ["DB_USER"],
            'password': os.environ["DB_PASS"],
            'database': os.environ["DB_NAME"]}

ITEM_PIPELINES = {'results_scraper.pipelines.PlayerPipeline': 100}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'HockeyML (+http://www.hockeyml.com)'

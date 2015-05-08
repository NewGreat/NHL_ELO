# This spider crawls the NHL League Schedule page.

from datetime import datetime
import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from results_scraper.items import *


# This spider grabs most classic stats from the 'Summary' pages.

class ScheduleSpider(CrawlSpider):
    # define class variables
    name = "schedule"
    allowed_domains = ["nhl.com"]
    start_urls = []

    def __init__(self, season="", *args, **kwargs):
        super(ScheduleSpider, self).__init__(*args, **kwargs)

        # allows the passing of the command line argument to parse_item method
        self.year = int(season)

        self.start_urls = [
            "http://www.nhl.com/ice/schedulebyseason.htm"
            "?season={0}{1}&gameType=2&team=&network=&venue=".format(self.year - 1, self.year)]

    def parse(self, response):
        sel = Selector(response)

        # collect xpaths of each team (row in table)
        rows = sel.xpath('/html//div[@class="contentBlock"]/table/tbody/tr')

        # define collection of teams that play in games we care about
        # (some teams have moved, but we still want the old games)
        # We'll grab the first four letters of the team to distinguish,
        # then assign the NHL's standard 3-letter code.

        TEAMS = {'Anah': 'ANA',
                 'Ariz': 'ARI',
                 'Calg': 'CGY',
                 'Edmo': 'EDM',
                 'Los ': 'LAK',
                 'San ': 'SJS',
                 'Vanc': 'VAN',
                 'Chic': 'CHI',
                 'Colo': 'COL',
                 'Dall': 'DAL',
                 'Minn': 'MIN',
                 'Nash': 'NAS',
                 'St. ': 'STL',
                 'Winn': 'WPG',
                 'Bost': 'BOS',
                 'Buff': 'BUF',
                 'Detr': 'DET',
                 'Flor': 'FLA',
                 'Mont': 'MTL',
                 'Otta': 'OTT',
                 'Tamp': 'TBL',
                 'Toro': 'TOR',
                 'Caro': 'CAR',
                 'Colu': 'CBJ',
                 'New ': 'NJD',
                 'NY I': 'NYI',
                 'NY R': 'NYR',
                 'Phil': 'PHI',
                 'Pitt': 'PIT',
                 'Wash': 'WAS',
                 'Phoe': 'ARI',
                 'Atla': 'WPG'}

        # loop through teams
        for row in rows:
            if row.xpath('td[1]/@colspan').extract()[0] == '1':
                loader = ItemLoader(PlayoffsItem(), selector=row)
                loader.default_input_processor = MapCompose()
                loader.default_output_processor = Join()

                # add season and date
                loader.add_value('season', str(self.year))
                date = datetime.strptime(row.xpath('td[1]/div[1]/text()').extract()[0][4:], '%b %d, %Y').date()
                loader.add_value('date', str(date))

                # get team identifiers
                away = ''
                if row.xpath('td[2]/a[1]/@rel').extract():
                    away = row.xpath('td[2]/a[1]/@rel').extract()[0]
                elif row.xpath('td[2]/div/text()').extract()[0][:4] in TEAMS:
                    away = TEAMS[row.xpath('td[2]/div/text()').extract()[0][:4]]
                if away:
                    if row.xpath('td[3]/a[1]/@rel').extract():
                        home = row.xpath('td[3]/a[1]/@rel').extract()[0]
                    else:
                        home = TEAMS[row.xpath('td[3]/div/text()').extract()[0][:4]]
                    loader.add_value('away', away)
                    loader.add_value('home', home)

                    # collect and parse results
                    away_score = row.xpath('td[5]/span[1]/text()').extract()[0].replace('\n', '').strip()
                    match = re.search('\(.*?\)', away_score)
                    loader.add_value('away_score', match.group(0)[1:-1])
                    home_score = row.xpath('td[5]/span[2]/text()').extract()[0].replace('\n', '').strip()
                    match = re.search('\(.*?\)', home_score)
                    loader.add_value('home_score', match.group(0)[1:-1])
                    match = re.search('\).*', home_score)
                    result = match.group(0)[1:]
                    if result == 'S/O':
                        output = 'SO'
                    elif result == 'OT':
                        output = 'OT'
                    else:
                        output = 'REG'
                    loader.add_value('result', output)

                    # feed item to pipeline
                    yield loader.load_item()
            else:
                pass
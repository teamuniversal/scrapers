# -*- coding: utf-8 -*-
# Universal Scrapers
import re, requests, time, urllib
import xbmcaddon, json, xbmc
from ..scraper import Scraper
from ..common import clean_title, filter_host, send_log, error_log
from ..modules import client, dom_parser, quality_tags

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class moviefull(Scraper):
    domains = ['cinebloom.com']
    name = "Cinebloom"
    sources = []

    def __init__(self):
        self.base_link = 'https://www.cinebloom.com/'
        self.search_url = self.base_link + 'search?q=%s'
        self.sources = []
        if dev_log == 'true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            search_id = urllib.quote_plus(title+' '+year)
            query = self.search_url % search_id
            print 'SEARCH URL: %s' % query
            item_url = self._search(query, title, year)

            self.get_source(item_url, title, year, '', '', start_time)

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            search_id = urllib.quote_plus(title + ' ' + year)
            query = self.search_url % search_id
            print 'SEARCH URL: %s' % query

            item_url = self._search(query, title, year)

            self.get_source(item_url, title, year, season, episode, start_time)

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, 'Check Search')
            return self.sources

    def _search(self, url, title, year):
        try:
            r = client.request(url)
            data = client.parseDOM(r, 'section', attrs={'class': 'search'})[0]
            data = client.parseDOM(data, 'li')
            for item in data:
                name = client.parseDOM(item, 'strong', attrs={'itemprop': 'name'})[0]
                item_url = client.parseDOM(item, 'a', ret='href')[0]
                #print '@#@(grabbed url) %s  (title) %s' % (item_url, name)
                if not clean_title(title).lower() == clean_title(name).lower():
                    continue
                if not year in name:
                    continue
                #print '@#@URL check> ' + item_url
                return item_url
        except:
            return


    def get_source(self, item_url, title, year, season, episode, start_time):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                       'Referer': item_url}
            r = client.request(item_url)
            if 'tvshows' in item_url: #for tvshows
                r = client.parseDOM(r, 'tr', attrs={'class': 'season'}) # find the seasons
                r = [i for i in r if 'season %s' % int(season) in i.lower()][0] #select season
                epis = client.parseDOM(r, 'li')# scrape all episodes
                epi = [i for i in epis if 'ep %s' % int(episode) in i.lower()][0] #select episode
                link = dom_parser.parse_dom(epi, 'a', req='href')[0]# scrape the link and the host label
                links = (link.attrs['href'], link.content)# create the link-hoster list

            else:
                # locate the streams list
                r = client.parseDOM(r, 'tbody', attrs={'id': 'stream-list'})[0]
                # scrape the links and the host label
                links = client.parseDOM(r, 'span', attrs={'class': 'stream-name'})
                links = [dom_parser.parse_dom(i, 'a', req='href') for i in links if i]
                # create the link-hoster list
                links = [(i[0].attrs['href'], re.sub('<.+?>', '', i[0].content)) for i in links if i]
                # pass the links on sources list
            count = 0
            for item in links:
                url = item[0]
                host = item[1]
                if 'whatever' in url:
                    link = client.request(url, headers=headers, output='geturl')
                elif 'spider' in url:
                    url = client.replaceHTMLCodes(url)
                    cj = client.request(item_url, output='cookie')
                    headers['Cookie'] = cj
                    r = client.request(url, headers=headers)
                    link = client.parseDOM(r, 'iframe', ret='src')[0]

                else:
                    r = client.request(url, headers=headers)
                    link = client.parseDOM(r, 'iframe', ret='src')[0]
                count += 1
                qual, info = quality_tags.get_release_quality(link, link)
                print '@#@FINAL-LINK: %s' % link
                if qual == 'SD':
                    r = client.request(link)
                    quality = client.parseDOM(r, 'meta', attrs={'name': 'description'},  ret='content')[0]
                    qual, info = quality_tags.get_release_quality(quality, quality)

                self.sources.append(
                    {'source': host, 'quality': qual, 'scraper': self.name, 'url': link, 'direct': False})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year, season='', episode='')
        except:
            pass
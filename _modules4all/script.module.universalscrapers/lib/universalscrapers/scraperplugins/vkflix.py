# -*- coding: utf-8 -*-
#Universal-Scraper checked 31/08/2018

import re, urllib, urlparse
import xbmc, xbmcaddon, time
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, clean_search, send_log, error_log
from universalscrapers.modules import client, quality_tags

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class vkflix(Scraper):
    domains = ['vkflix.net']
    name = "VKFlix"
    sources = []

    def __init__(self):
        self.base_link = 'http://vkflix.net/'
        self.search_link = 'search?q=%s'
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            search_id = clean_search(title.lower())
            #print search_id
            #xbmc.log('@#@TITLE: %s' % search_id, xbmc.LOGNOTICE)
            start_url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(search_id))
            headers = {'User-Agent': client.agent()}

            r = client.request(start_url, headers=headers)
            posts = client.parseDOM(r, 'div', attrs={'id': 'movie-\d+'})
            posts = [(client.parseDOM(i, 'h4')[0]) for i in posts if i]
            #print posts
            posts = [(client.parseDOM(i, 'a', ret='href')[0],
                      client.parseDOM(i, 'a')[0]) for i in posts if i]

            #posts = [(i[0]) for i in posts if clean_title(search_id) == clean_title(i[1])]
            count = 0
            for link, found_title in posts:
                link = urlparse.urljoin(self.base_link, link) if link.startswith('/') else link
                if not clean_title(title) == clean_title(found_title): continue
                result = client.request(link, headers=headers)
                y = client.parseDOM(result, 'div', attrs={'class': 'showValue showValueRelease'})[0]
                if not year == y: continue

                streams = client.parseDOM(result, 'div', attrs={'class': 'linkTr'})
                for stream in streams:
                    quality = client.parseDOM(stream, 'div', attrs={'class': 'linkQualityText'})[0]
                    link = client.parseDOM(stream, 'div', attrs={'class':'linkHidden linkHiddenUrl'})[0]
                    #print link

                    if 'vidnode' in link:
                        continue

                    if 'HD' in quality:
                        quality = 'HD'
                    else:
                        quality = 'SD'

                    host = quality_tags._give_host(link)
                    #print host
                    count += 1
                    self.sources.append(
                        {'source': host, 'quality': quality, 'scraper': self.name, 'url': link, 'direct': False})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year)
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            search_id = clean_search(title.lower())
            start_url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(search_id))
            #print start_url
            headers = {'User-Agent': client.agent()}

            r = client.request(start_url, headers=headers)
            posts = client.parseDOM(r, 'div', attrs={'id': 'movie-\d+'})
            posts = [(client.parseDOM(i, 'h4')[0]) for i in posts if i]
            for item in posts:
                name = client.parseDOM(item, 'a')[0]
                link = client.parseDOM(item, 'a', ret='href')[0]
                if not clean_title(title) == clean_title(name): continue

                link = urlparse.urljoin(self.base_link, link)
                html = client.request(link)
                #<div class="season" id="season8">
                sep_id = 'Season %s Serie %s' % (int(season), int(episode))
                #print sep_id
                seasons = client.parseDOM(html, 'div', attrs={'class': 'season'})
                seasons = [i for i in seasons if 'season %s' % int(season) in i.lower()][0]

                epis = re.findall('<h3>(.+?)</div>\s+</div>\s+</div>\s+</div>', seasons, re.DOTALL | re.MULTILINE)
                epis = [i for i in epis if sep_id in i][0]

                count = 0
                streams = client.parseDOM(epis, 'div', attrs={'class': 'linkTr'})
                for stream in streams:
                    quality = client.parseDOM(stream, 'div', attrs={'class': 'linkQualityText'})[0]
                    link = client.parseDOM(stream, 'div', attrs={'class': 'linkHidden linkHiddenUrl'})[0]
                    #print link

                    if 'vidnode' in link:
                        continue

                    if 'HD' in quality:
                        quality = 'HD'
                    else:
                        quality = 'SD'

                    host = quality_tags._give_host(link)
                    # print host
                    count += 1
                    self.sources.append(
                        {'source': host, 'quality': quality, 'scraper': self.name, 'url': link, 'direct': False})

                if dev_log == 'true':
                    end_time = time.time() - start_time
                    send_log(self.name, end_time, count, title, year, season=season, episode=episode)

            return self.sources
        except Exception as argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return []


#vkflix().scrape_movie('Black Panther', '2018', '', False)
#vkflix().scrape_episode('Suits', '2011','','8','5','','')
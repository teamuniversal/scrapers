# -*- coding: utf-8 -*-
# Bugatsinho for Universal Scrapers

import xbmcaddon
import time
import re
import urllib, urlparse

from universalscrapers.common import send_log, error_log, clean_search, clean_title
from universalscrapers.scraper import Scraper
from universalscrapers.modules import client, quality_tags

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class filepursuit(Scraper):
    domains = ['filepursuit.com']
    name = "filuit"
    sources = []

    def __init__(self):
        self.base_link = 'https://filepursuit.com'
        self.search_links = ['/search4/%s/type/videos/', '/search4/%s/type/videos/startrow/49/',
                             '/search4/%s/type/videos/startrow/98', '/search4/%s/type/videos/startrow/147']

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            query = clean_search(title)
            query = urllib.quote_plus(query + ' ' + year)
            urls = []
            for link in self.search_links:
                try:
                    url = urlparse.urljoin(self.base_link, link % query)
                    url = urlparse.urljoin(self.base_link, url)
                    r = client.request(url)
                    posts = client.parseDOM(r, 'tbody')
                    posts = client.parseDOM(posts, 'tr')
                    urls += [(client.parseDOM(i, 'button', ret='data-clipboard-text')[0]) for i in posts if i]
                except:
                    pass
            count = 0
            for url in urls:
                name = url.split('/')[-1].lower()
                name = client.replaceHTMLCodes(name).replace('%20', '')
                if any(x in url for x in ['italian', 'dubbed', 'teaser', 'subs', 'sub', 'dub',
                                           'samples', 'extras', 'french', 'trailer', 'trailers', 'sample']):
                    continue
                t = re.sub('(\.|\(|\[|\s)(\d{4}|3D)(\.|\)|\]|\s)(.+|)', '', name, flags=re.I)
                if clean_title(t) not in clean_title(title): continue
                y = re.findall('[\.|\(|\[|\s](\d{4})[\.|\)|\]|\s]', name, re.I)[-1].upper()
                if not year == y: continue

                res, info = quality_tags.get_release_quality(name, url)
                if any(x in url for x in ['hastidl', '1tehmovies', '62.210.103.107', '79.127', '213.32.113.82',
                                          'dl5.downloadha', '89.163.255.42', '185.56.20.142', 's1.0music',
                                          'dl3.yoozdl', 'dl4.lavinmovie.net', 'dl6.lavinmovie.net',
                                          'dl3.upload08.com', 'dl8.uploadt.com',
                                          '163.172.6.218', 'samba.allunix.ru', 'server417']):
                    count += 1

                    url += '|User-Agent=%s&Referer=%s' % (client.agent(), self.base_link)
                    url = urllib.quote(url, '|:?/&+=_-')

                    self.sources.append(
                        {'source': 'DirectLink', 'quality': res, 'scraper': self.name, 'url': url, 'direct': True})

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
            hdlr = 'S%02dE%02d' % (int(season), int(episode))
            query = clean_search(title)
            query = urllib.quote_plus(query + ' ' + hdlr)
            urls = []
            for link in self.search_links:
                try:
                    url = urlparse.urljoin(self.base_link, link % query)
                    url = urlparse.urljoin(self.base_link, url)
                    r = client.request(url)
                    posts = client.parseDOM(r, 'tbody')
                    posts = client.parseDOM(posts, 'tr')
                    urls += [(client.parseDOM(i, 'button', ret='data-clipboard-text')[0]) for i in posts if i]
                except:
                    pass
            count = 0
            for url in urls:
                name = url.split('/')[-1].lower()
                name = client.replaceHTMLCodes(name).replace('%20', '')
                if 'movies' in url:
                    continue
                if any(x in url for x in ['italian', 'dubbed', 'teaser', 'subs', 'sub', 'dub',
                                          'samples', 'extras', 'french', 'trailer', 'trailers', 'sample']):
                    continue

                t = re.sub('(\.|\(|\[|\s)(S\d+E\d+|S\d+)(\.|\)|\]|\s)(.+|)', '', name, flags=re.I)
                if clean_title(t) not in clean_title(title): continue
                y = re.findall('[\.|\(|\[|\s](S\d+E\d+|S\d+)[\.|\)|\]|\s]', name, re.I)[-1].upper()
                if not y == hdlr: continue

                res, info = quality_tags.get_release_quality(name, url)

                if any(x in url for x in ['hastidl', '1tehmovies', '62.210.103.107', '79.127', '213.32.113.82',
                                          'dl5.downloadha', '89.163.255.42', '185.56.20.142', 's1.0music',
                                          'dl3.yoozdl', 'dl4.lavinmovie.net', 'dl6.lavinmovie.net',
                                          'dl3.upload08.com', 'dl8.uploadt.com', '163.172.6.218',
                                          'samba.allunix.ru', 'server417']):
                    count += 1

                    url += '|User-Agent=%s&Referer=%s' % (client.agent(), self.base_link)
                    url = urllib.quote(url, '|:?/&+=_-')

                    self.sources.append(
                        {'source': 'DirectLink', 'quality': res, 'scraper': self.name, 'url': url, 'direct': True})

            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year)

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources



#filepursuit().scrape_movie('Black Panther', '2018', '')
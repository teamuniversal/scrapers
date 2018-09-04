# -*- coding: utf-8 -*-

import requests, urllib, urlparse
import re, xbmcaddon, time
from ..scraper import Scraper
from ..common import clean_title, send_log, error_log
from ..modules import client, quality_tags

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")
s = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
                                           
class joymovies(Scraper):
    domains = ['oceanofmovies.bz']
    name = "OceanofMovies"
    sources = []

    def __init__(self):
        self.base_link = 'http://oceanofmovies.info'
        self.search_link = '/search/%s/feed/rss2/'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            search_id = '%s %s' % (title, year)
            start_url = self.base_link + self.search_link % urllib.quote_plus(search_id)
            #print 'STARTURL:::::::::::::::: '+start_url
            headers = {'User-Agent': User_Agent}

            r = client.request(start_url, headers=headers)
            items = client.parseDOM(r, 'item')
            for item in items:
                name = re.search('Movie\s*Name\s*:\s*(.+?)<br', item, re.DOTALL).groups()[0]
                name = client.replaceHTMLCodes(name)
                t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d+E\d+|S\d+|3D)(\.|\)|\]|\s|)(.+|)', '', name, flags=re.I)

                if not clean_title(title) == clean_title(t):
                    continue
                if not year in name:
                    continue

                self.get_source(item, title, year, '', '', start_time)

            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

    def get_source(self, item_url, title, year, season, episode, start_time):
        try:
            #print '%s %s %s' %(item_url,title,year)
            headers={'User-Agent':User_Agent}

            qual = re.search('uality\s*:(.+?)<br', item_url, re.DOTALL).groups()[0]
            qual, info = quality_tags.get_release_quality(qual, qual)

            count = 0
            headers = {'Origin': self.base_link, 'Referer': client.parseDOM(item_url, 'link')[0],
                       'X-Requested-With': 'XMLHttpRequest', 'User_Agent': User_Agent}
            try:
                fn = client.parseDOM(item_url, 'input', attrs={'name': 'FName'}, ret='value')[0]
                fs = client.parseDOM(item_url, 'input', attrs={'name': 'FSize'}, ret='value')[0]
                fsid = client.parseDOM(item_url, 'input', attrs={'name': 'FSID'}, ret='value')[0]
                #params = re.compile('<input name="FName" type="hidden" value="(.+?)" /><input name="FSize" type="hidden" value="(.+?)" /><input name="FSID" type="hidden" value="(.+?)"').findall(html)

                post_url = self.base_link + '/thanks-for-downloading/'
                form_data = {'FName': fn, 'FSize': fs, 'FSID': fsid}
                #link = requests.post(request_url, data=form_data, headers=headers).content
                link = client.request(post_url, post=form_data, headers=headers)

                stream_url = client.parseDOM(link, 'meta', attrs={'http-equiv': 'refresh'}, ret='content')[0]
                stream_url = re.search('url=(.+?)"', stream_url, re.DOTALL).groups()[0]
            except:
                pass
            stream_url = client.replaceHTMLCodes(stream_url)#stream_url.replace('#038;','')
            count +=1
            self.sources.append({'source': 'DirectLink', 'quality': qual, 'scraper': self.name,'url': stream_url, 'direct': True})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year, season=season,episode=episode)                               
        except:
            pass
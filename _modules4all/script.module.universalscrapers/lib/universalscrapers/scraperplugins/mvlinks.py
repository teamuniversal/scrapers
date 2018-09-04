# -*- coding: utf-8 -*-

import re, xbmcaddon, time
import resolveurl, requests, urllib
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log
from ..modules import client, quality_tags, workers
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'


class mvlinks(Scraper):
    domains = ['http://dl.newmyvideolink.xyz/dl']
    name = "MyVideoLinks"
    sources = []

    def __init__(self):
        self.base_link = 'http://iwantmyshow.tk/'
        self.search_link = 'new/?s=%s'
        self.count = 0

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_time = time.time()

            #season_pull = '%02d' % int(season) #"0%s"%season if len(season)<2 else season
            #episode_pull = '%02d' % int(episode) #"0%s"%episode if len(episode)<2 else episode
            sepi = 'S%02dE%02d' % (int(season), int(episode))
            search_id = '%s %s' % (title, sepi)
                   
            movie_url = self.base_link + self.search_link % urllib.quote_plus(search_id)
            #print ' ##MOVIE URL##  %s' % movie_url
            headers = {'User_Agent':User_Agent}
            r = client.request(movie_url, headers=headers)
            items = client.parseDOM(r, 'article', attrs={'id': 'post-\d+'})
            for item in items:
                name = client.parseDOM(item, 'a')[0]
                name = client.replaceHTMLCodes(name)
                t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d+E\d+|S\d+|3D)(\.|\)|\]|\s|)(.+|)', '', name, flags=re.I)
                if not clean_title(title).lower() in clean_title(t).lower():
                    continue

                y = re.findall('[\.|\(|\[|\s](S\d*E\d*|S\d*)[\.|\)|\]|\s]', name, flags=re.I)[-1].upper()

                if y not in sepi:
                    continue

                link = client.parseDOM(item, 'a', ret='href')[0]

                if not y == sepi:
                    link = link
                else:
                    link += '2' if link.endswith('/') else '/2'
                #print ' ##final Item to pass## %s' % link
                self.get_source(link, title, year, season, episode, start_time)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources
        
    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            search_id = '%s %s' % (title, year)
            movie_url = self.base_link + self.search_link % urllib.quote_plus(search_id)
            headers = {'User_Agent': User_Agent}
            
            r = client.request(movie_url, headers=headers)
            items = client.parseDOM(r, 'article', attrs={'id': 'post-\d+'})
            links = []
            for item in items:
                name = client.parseDOM(item, 'a')[0]
                name = client.replaceHTMLCodes(name)
                t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d+E\d+|S\d+|3D)(\.|\)|\]|\s|)(.+|)', '', name, flags=re.I)

                if not clean_title(title) == clean_title(t):
                    continue
                if not year in name:
                    continue
                link = client.parseDOM(item, 'a', ret='href')[0]
                link += '/2/'
                links.append(link)

            threads = []
            for i in links: threads.append(workers.Thread(self.get_source, i, title, year, '', '', start_time))
            [i.start() for i in threads]

            alive = [x for x in threads if x.is_alive() is True]
            while alive:
                alive = [x for x in threads if x.is_alive() is True]
                time.sleep(0.1)

            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def get_source(self, m_url, title, year, season, episode, start_time):
        #import xbmc
        try:
            hdlr = 'S%02dE%02d' % (int(season), int(episode)) if not season == '' else year
            r = client.request(m_url)
            if not hdlr in m_url.upper():
                quality = client.parseDOM(r, 'h4')[0]
                regex = '<p>\s*%s\s*</p>(.+?)</ul>' % hdlr
                data = re.search(regex, r, re.DOTALL | re.I).groups()[0]
                frames = client.parseDOM(data, 'a', ret='href')

            else:
                data = client.parseDOM(r, 'div', attrs={'class': 'entry-content'})[0]
                data = re.compile('<h4>(.+?)</h4>(.+?)</ul>', re.DOTALL).findall(data)
                #xbmc.log('DATAAAA:%s' % data, xbmc.LOGNOTICE)
                frames = []
                for qual, links in data:
                    quality = qual
                    frames += client.parseDOM(links, 'a', ret='href')

            for link in frames:
                if not resolveurl.HostedMediaFile(link).valid_url():
                    continue
                host = link.split('//')[1].replace('www.', '')
                host = host.split('/')[0].split('.')[0].title()
                if 'filebebo' in link: continue
                rez, info = quality_tags.get_release_quality(quality, link)
                if '1080p' in rez and not host.lower() in ['openload', 'oload']:
                    rez = '720p'
                elif '720p' in quality and not host.lower() in ['openload', 'oload']:
                    rez = 'SD'
                else:
                    rez, info = quality_tags.get_release_quality(link, link)

                self.count += 1
                self.sources.append({'source': host, 'quality': rez, 'scraper': self.name, 'url': link, 'direct': False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, self.count, title, year, season=season, episode=episode)

        except:
            pass

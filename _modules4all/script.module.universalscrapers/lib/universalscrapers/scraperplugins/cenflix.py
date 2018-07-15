# -*- coding: utf-8 -*-

import re, urllib, urlparse, json
import resolveurl as urlresolver
import xbmcaddon, time

from ..scraper import Scraper
from ..modules import cfscrape, client, unjuice
from ..modules.dom_parser import parse_dom as dom
from ..common import clean_title, send_log, error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class cenflix(Scraper):
    domains = ['moviego.cx']
    name = "CenFlix"
    sources = []

    def __init__(self):
        self.base_link = 'https://moviego.cx'
        self.search_link = '/?s=%s'

    def scrape_movie(self, title, year, imdb, debrid = False):
        #try:
            start_time = time.time()
            scraper = cfscrape.create_scraper()
            search_id = urllib.quote_plus(title)

            start_url = urlparse.urljoin(self.base_link, self.search_link % search_id)
            #print 'scrapercheck - scrape_movie - start_url:  ' + start_url
            
            headers={'User-Agent': client.agent()}
            html = scraper.get(start_url, headers=headers).content
            #match = re.compile('class="result-item".+?href="(.+?)".+?alt="(.+?)".+?class="year">(.+?)</span>',re.DOTALL).findall(html)
            match = client.parseDOM(html, 'div', attrs={'class': 'result-item'})
            match = [(dom(i, 'a', req='href')[1],
                      dom(i, 'span', {'class': 'year'})[0]) for i in match if i]

            match = [(i[0].attrs['href'], i[0].content, i[1].content) for i in match if i]

            for item_url, name, rel in match:
                #print 'scrapercheck - scrape_movie - name: '+name + '   '+rel
                #print 'scrapercheck - scrape_movie - item_url: '+item_url                                                           
                if not clean_title(title) == clean_title(name): continue
                if not rel == year: continue
                                                                                        
                print 'scrapercheck - scrape_movie - Send this URL: ' + item_url
                self.get_source(item_url, title, year, start_time)
            return self.sources
        #except Exception, argument:
            #if dev_log=='true':
             #   error_log(self.name,argument)

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_time = time.time()
            scraper = cfscrape.create_scraper()
            seaepi_chk = '%sx%s' %(season,episode)
            search_id = urllib.quote_plus(title)
            start_url = urlparse.urljoin(self.base_link, self.search_link % search_id)
            headers={'User-Agent': client.agent()}
            html = scraper.get(start_url, headers=headers, timeout=10).content
            #print html
            #match = re.compile('class="result-item".+?href="(.+?)".+?alt="(.+?)"',re.DOTALL).findall(html)
            match = client.parseDOM(html, 'div', attrs={'class': 'result-item'})
            match = dom(match, 'a', req='href')[1]
            match = [(i[0].attrs['href']) for i in match if clean_title(title) == clean_title(i[0].content)][0]
                #print tvshow_url +' '+ title

            tvshow = re.findall('tvshows/(.+?)/', match)[0]
            epi_link = self.base_link + 'episodes/%s-%s/' % (tvshow, seaepi_chk)

            self.get_source(epi_link, title, year, start_time)
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)

    def get_source(self, item_url, title, year, start_time):
        try:
            print 'PASSEDURL >>>>>>'+item_url
            scraper = cfscrape.create_scraper()
            count = 0
            headers={'User-Agent': client.agent()}
            OPEN = scraper.get(item_url, headers=headers, timeout=10).content
            links = client.parseDOM(OPEN, 'div', attrs={'class': 'playex'})[0]
            links = client.parseDOM(links, 'iframe', ret='src')

            print '@#@LINKS: %s' % links
            for link in links:
                # print link +'    ::::::::::::::::::::::'
                if 'sibeol' in link:
                    print 'SIBEOL LINK??????????????' + link
                    r = scraper.get(link, headers=headers, timeout=10).content
                    # print get_link_page + 'UNJUICE?????????????????'
                    # juicify = re.compile('>JuicyCodes.Run\("(.+?)\)\;\<',re.DOTALL).findall(get_link_page)
                    data = unjuice.run(r)
                    data = re.findall('sources:([^]]+\])', data, re.DOTALL)[0]
                    data = json.loads(data)
                    data = [(i['file'], i['label']) for i in data if data]
                    for end_url, rez in data:

                        if '/link/' in end_url:
                            if '1080' in rez:
                                qual = '1080p'
                            elif '720' in rez:
                                qual ='720p'
                            else:
                                qual = 'SD'
                            count += 1
                            end_url = '%s|User_Agent=%s&Referer=%s' % (end_url, client.agent(), item_url)
                            self.sources.append({'source': 'DirectLink', 'quality': qual, 'scraper': self.name, 'url':end_url, 'direct': True})
                else:
                    if urlresolver.HostedMediaFile(link):
                        count += 1
                        host = link.split('//')[1].replace('www.','')
                        host = host.split('/')[0].split('.')[0].title()
                        self.sources.append({'source': host, 'quality': 'DVD', 'scraper': self.name, 'url': link, 'direct':False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return[]
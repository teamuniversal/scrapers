# -*- coding: utf-8 -*-
# Universal Scrapers
# checked 30/8/2018 -BUG

import re, urllib
import xbmc, xbmcaddon, time
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, filter_host, clean_search, send_log, error_log
from universalscrapers.modules import client

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class hdvix(Scraper):
    domains = ['hdvix.com']
    name = "HDvix"
    sources = []

    def __init__(self):
        self.base_link = 'https://hdfun.net' #hdvix is a mirror. this site has 2 links
        self.search_link = '/search/%s/feed/rss2/'
        
    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()                                                   
            search_id = urllib.quote_plus('%s %s' % (clean_search(title), year))
            start_url = '%s/?s=%s' % (self.base_link, search_id)
            #print 'scraperchk - scrape_movie - start_url:  ' + start_url
            html = client.request(start_url)
            match = re.compile('class="thumb".+?title="(.+?)".+?href="(.+?)">',re.DOTALL).findall(html)
            for name, item_url in match:
                #print 'scraperchk - scrape_movie - name: '+name
                if not year in name:
                    continue
                if clean_title(title) == clean_title((name.split(year)[0][:-1])):
                    #print 'scraperchk - scrape_movie - Send this URL: ' + item_url
                    self.get_source(item_url, title, year, start_time)
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources
    # def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
    #     try:
    #         start_time = time.time()
    #         season_chk = '-season-%s' %(season)
    #         #print season_chk
    #         search_id = clean_search(title.lower())
    #         start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
    #         headers={'User-Agent':random_agent()}
    #         html = requests.get(start_url,headers=headers,timeout=5).content
    #         match = re.compile('class="ml-item".+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
    #         for season_url, title in match:
    #             #print season_url
    #             if not season_chk in season_url:
    #                 continue
    #             #print 'PASSED season URL### ' +season_url
    #             episode_grab = 'Season %s Episode %s ' %(season,episode)

    #             item_url = self.base_link+season_url+'/watching.html'
    #             html=requests.get(item_url, headers=headers, timeout=5).content
    #             match = re.compile('<a title="(.+?)" player-data="(.+?)"',re.DOTALL).findall(html)
    #             for epi, link in match:
    #                 epi = epi.split('-')[1].split('-')[0]

    #                 if not clean_title(epi).lower() == clean_title(episode_grab).lower():
    #                     continue
    #                 #print 'Passed episode > '+epi
    #                 #if link.startswith('://vidnode.net/'):
    #                     #link = link.replace('://vidnode.net/','https://vidnode.net/')
    #                 if link.startswith('//vidnode.net/'):
    #                     link = link.replace('//vidnode.net/','https://vidnode.net/')
    #                 #print 'matched link>>> ' + link
    #                 host = link.split('//')[1].replace('www.','')
    #                 host = host.split('/')[0].split('.')[0].title()

    #                 self.sources.append({'source':host, 'quality':'SD', 'scraper':self.name, 'url':link, 'direct':False})
    #             return self.sources
    #     except Exception, argument:
    #         if dev_log=='true':
    #             error_log(self.name,argument) 


    def get_source(self,item_url,title,year,start_time):
        try:
            #print 'PASSEDURL >>>>>>'+item_url
            count = 0
            OPEN = client.request(item_url)
            links = client.parseDOM(OPEN, 'iframe', ret='src')

            for link in links:
                #print link+'<<<<<<<<<<<<<<<<<<<<<<<<<<'

                host = link.split('//')[1].replace('www.', '')
                host = host.split('/')[0].lower()
                if not filter_host(host): continue

                count += 1
                self.sources.append({'source': host, 'quality': 'HD', 'scraper': self.name, 'url': link, 'direct': False})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year)
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)


#hdvix().scrape_movie('Black Panther', '2018', 'tt1825683', False)
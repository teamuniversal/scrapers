import re,time
import xbmcaddon
import urllib
import requests

from ..common import clean_title,clean_search, random_agent,filter_host,send_log,error_log
from ..scraper import Scraper

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4'

## 403 ??? try with session req
class fanstashtv(Scraper):
    domains = ['http://fanstashtv.org/']
    name = "FanStashTV"

    def __init__(self):
        self.base_link = 'http://fanstashtv.org/'
        self.sources = []
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s?s=%s' %(self.base_link,search_id.replace(' ','+'))
            print '~~~~~~~~~~~start url'+start_url
            headers = {'User_Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
            print html
            Regex = re.compile('class="td-module-thumb".+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
            for item_url,name in Regex:
                #print item_url+'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
                #print name+'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
                if clean_title(title).lower() == clean_title(name).lower():
                    headers = {'User_Agent':User_Agent}
                    OPEN= requests.get(item_url,headers=headers,timeout=5).content
                    grab= re.compile('class="td-module-thumb".+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(OPEN)
                    for show_link,check in grab:
                        if len(season)>1 and season.startswith('0'): ss = season[1:]

                        else: 
                            if len(season)>1 and not season.startswith('0'): ss = season
                        if len(episode)>1 and episode.startswith('0'): ee = episode[1:]

                        else: 
                            if len(episode)>1 and not episode.startswith('0'): ee = episode
                        
                        checks=check.replace(' ','')+'<'
                        info = re.compile('Season(.+?)Episode(.+?)<').findall(str(checks))
                        for seas,eps in info:
                            if ee == eps and ss == seas:
                                
                                self.get_sources(show_link)
 
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def get_sources(self, show_link):
        print '::::::::::::::'+show_link
        try:
            headers = {'User_Agent':User_Agent}
            link1 = requests.get(show_link,headers=headers,timeout=5).content   
            ENDLINK = re.compile('<IFRAME SRC="(.+?)"',re.DOTALL).findall(link1)
            count = 0            
            for link in ENDLINK:
                print link
                if '1080' in link:
                    label = '1080p'
                elif '720' in link:
                    label = '720p'
                else:
                    label = 'SD'
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                self.sources.append({'source': host,'quality': 'DVD','scraper': self.name,'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)
    

        except:pass

#fanstashtv().scrape_episode('the crown', '2018', '', '02', '02', '', '')
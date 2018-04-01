import re
import requests,time
import xbmc,xbmcaddon
import urllib
from ..scraper import Scraper
from ..common import clean_title, random_agent, clean_search,send_log,error_log
requests.packages.urllib3.disable_warnings()

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

session = requests.Session()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

class flenix(Scraper):
    domains = ['https://flenix.co']
    name = "Flenix"
    sources = []

    def __init__(self):
        self.base_link = 'https://flenix.co'
        self.goog = 'https://www.google.co.uk'
        self.sources = []
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
        
            scrape = clean_search(title.lower()).replace(' ','+')

            start_url = '%s/search?q=flenix.co+%s+%s' %(self.goog,scrape,year)

            headers = {'User-Agent':random_agent()}

            html = requests.get(start_url,headers=headers).content

            results = re.compile('href="(.+?)"',re.DOTALL).findall(html)
            count = 0
            for url in results:
                if  self.base_link in url and scrape.replace('+','-') in url and 'google' not in url:
                    #continue
                    #print url
                    page = session.get(url,headers=headers).content
                    match = re.compile('type:.+?src:.+?"(.+?)"',re.DOTALL).findall(page)
                    for link in match:
                        #print link
                        count +=1
                        link = link
                        self.sources.append({'source': 'DirectLink','quality': '720P','scraper': self.name,'url': link,'direct': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)            
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources



#flenix().scrape_movie('coco', '2017','')
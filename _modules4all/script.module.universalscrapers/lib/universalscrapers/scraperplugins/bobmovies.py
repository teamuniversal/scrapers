import re,time,requests
import xbmcaddon
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log    
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")           
requests.packages.urllib3.disable_warnings()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
class bobmovies(Scraper):
    domains = ['https://bobmovies.online']
    name = "Bobmovies"
    sources = []

    def __init__(self):
        self.base_link = 'https://bobmovies.online'
        self.goog = 'https://www.google.com/search?q=bobmovies.online+'
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            scrape = clean_search(title.lower())
            google = '%s%s'%(self.goog,scrape.replace(' ','+'))
            #print google
            get_page = requests.get(google).content

            match = re.compile('<a href="(.+?)"',re.DOTALL).findall(get_page)
            for url1 in match:
                #print url1
                if '/url?q=' in url1:
                    if self.base_link in url1 and 'google' not in url1:
                        url2 = url1.split('/url?q=')[1]
                        url2 = url2.split('&amp')[0]
                        #print url2
                        headers={'User-Agent':User_Agent}
                        html = requests.get(url2,headers=headers,timeout=5).content
                        #print html
                        results = re.compile('<div class="page_film_top full_film_top">.+?<h1>(.+?)</h1>.+?<td class="name">Quality:</td><td><a href=.+?">(.+?)</a>.+?<td class="name">Year:</td><td><a href=.+?">(.+?)</a>',re.DOTALL).findall(html)
                        for item_title, qual, date  in results:
                            #print item_title+'>>>>>>>'+date
                            if not clean_title(title).lower() == clean_title(item_title).lower():
                                continue
                            if not year in date: 
                                continue
                            self.get_source(url2,title,year,'','',start_time,qual)
                        
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

    def get_source(self,url,title,year,season,episode,start_time,qual):
        try:
            headers={'User-Agent':random_agent()}
            html = requests.get(url,headers=headers,timeout=5).content
            
            vidpage = re.compile('id="tab-movie".+?data-file="(.+?)"',re.DOTALL).findall(html)
            count = 0
            for link in vidpage:
                if 'trailer' not in link.lower():
                    link = self.base_link + link
                    count +=1
                    self.sources.append({'source': 'DirectLink','quality': qual,'scraper': self.name,'url': link,'direct': True})
            other_links = re.findall('data-url="(.+?)"',html)
            for link in other_links:
                #print link
                if link.startswith('//'):
                    link = 'http:'+link
                count +=1
                self.sources.append({'source': 'DirectLink','quality': qual,'scraper': self.name,'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year, season='',episode='')                          
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

#bobmovies().scrape_movie('logan', '2017','')


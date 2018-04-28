import re,time,requests
import xbmcaddon
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log    
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")           

class bobmovies(Scraper):
    domains = ['https://bobmovies.online']
    name = "Bobmovies"
    sources = []

    def __init__(self):
        self.base_link = 'https://bobmovies.online'
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            scrape = clean_search(title.lower())
            
            headers = {'User-Agent':random_agent(),'referrer':self.base_link}
            
            data = {'do':'search','subaction':'search','story':scrape}
        	
            html = requests.post(self.base_link,headers=headers,data=data,verify=False,timeout=5).content
            
            results = re.compile('class="nnoo short_story".+?href="(.+?)".+?class="genre short_story_genre">(.+?)</span>.+?<p>(.+?)</p>',re.DOTALL).findall(html)
            for url,date,item_title in results:
            	#print item_title+'>>>>>>>'+date+'.....'+url
                if not clean_title(title).lower() == clean_title(item_title).lower():
                    continue
                if not year in date: 
                    continue
                self.get_source(url,title,year,'','',start_time)
                        
            print self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

    def get_source(self,url,title,year,season,episode,start_time):
        try:
            headers={'User-Agent':random_agent()}
            html = requests.get(url,headers=headers,timeout=5).content
            
            vidpage = re.compile('id="tab-movie".+?data-file="(.+?)"',re.DOTALL).findall(html)
            count = 0
            for link in vidpage:
                if 'trailer' not in link.lower():
                    link = self.base_link + link
                    count +=1
                    self.sources.append({'source': 'DirectLink','quality': '720p','scraper': self.name,'url': link,'direct': False})
            other_links = re.findall('data-url="(.+?)"',html)
            for link in other_links:
                print link
                if link.startswith('//'):
                    link = 'http:'+link
                count +=1
                self.sources.append({'source': 'DirectLink','quality': 'unknown','scraper': self.name,'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year, season='',episode='')                          
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

#bobmovies().scrape_movie('Jumanji: Welcome to the jungle', '2017','')


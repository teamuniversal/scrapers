import requests,re,time,xbmcaddon
import base64
from ..scraper import Scraper
from universalscrapers.modules import cfscrape
from ..common import clean_title,clean_search,random_agent,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")  

class extramovies(Scraper):
    domains = ['http://extramovies.cc/']
    name = "extramovies"
    sources = []

    def __init__(self):
        self.base_link = 'http://extramovies.cc'
        self.scraper = cfscrape.create_scraper()


    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower()) 
            start_url = self.base_link + '/?s=' +search_id.replace(' ','+')
            headers={'User-Agent':random_agent()}
            html = self.scraper.get(start_url,headers=headers,timeout=5).content 
            match = re.compile('class="thumbnail">.+?href="(.+?)" title="(.+?)".+?class="rdate">(.+?)</span>.+?</article>',re.DOTALL).findall(html) # Regex info on results page
            for item_url, name ,release in match:
                release = release.strip()
                if year == release:
                    if year in release:
                        self.get_source(item_url)
            return self.sources
        except:
            pass
            return[]

            
    def get_source(self,item_url):
        try:
                headers={'User-Agent':random_agent()}
                OPEN = requests.get(item_url,headers=headers,timeout=5).content
                block = re.compile('Single Download Links</b>(.+?)class="crp_related',re.DOTALL).findall(OPEN)
                Endlinks = re.compile('<a href="(.+?)="_blank" rel="noopener">(.+?)</a>',re.DOTALL).findall(str(block))
                count = 0
                for start_link,host in Endlinks:
                    mid_link = re.compile('.+?;link=(.+?)" target',re.DOTALL).findall(str(start_link))
                    for finished_link in mid_link:
                        link = base64.decodestring(finished_link)
                        print link
                        print host
                        count +=1    
                    self.sources.append({'source': host, 'quality': 'UnKnown', 'scraper': self.name, 'url': link,'direct': True}) #this line will depend what sent     
                if dev_log=='true':
                        end_time = time.time() - self.start_time
                        send_log(self.name,end_time,count)
        except:
            pass
# extramovies().scrape_movie('justice league', '2017','')
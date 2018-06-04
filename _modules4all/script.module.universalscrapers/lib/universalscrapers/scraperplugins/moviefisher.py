import requests
import re
import xbmcaddon
import xbmc
import time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")
  
class moviefishers(Scraper):
    domains = ['http://moviefishers.org']
    name = "moviefishers"
    sources = []

    def __init__(self):
        self.base_link = 'http://moviefishers.org'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            search_id = clean_search(title.lower())                                     # use 'clean_search' to get clean title                                                                              #(movie name keeping spaces removing excess characters)
            start_url = "http://moviefishers.org/wp-json/wp/v2/posts?search="+search_id.replace(' ','+')
            self.get_source(start_url,title,year,start_time)                        
            return self.sources
        except Exception as E:
            xbmc.log(str(E),2)
                        
    def get_source(self,item_url,title,year,start_time):
            data = requests.get(item_url).json()
            for item in data:
                title = item["title"]["rendered"]
                content = item["content"]["rendered"]
                year2 = item["date"][:4]
                if int(year) != int(year2):
                    continue
                Links = re.findall(r"(http.*streamango.com\/embed\/\w{1,}|https:\/\/openload\.co\/embed\/\w{1,}\/)",content)
                for link in Links:
                    host = re.findall(r"https:/\/(.*)\.",link)[0]
                    label = "DVD"
                    self.sources.append({'source': host, 'quality': label, 'scraper': self.name, 'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)       

# moviefishers().scrape_movie('tiger zinda hai', '2018','')
# you will need to regex/split or rename to get host name if required from link unless available on page it self 

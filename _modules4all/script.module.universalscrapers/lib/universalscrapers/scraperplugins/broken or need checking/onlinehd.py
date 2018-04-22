import re
import requests
import xbmc
from ..scraper import Scraper
from ..common import clean_search, clean_title
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
### sessions maybe
class OnlineHDWatch(Scraper):
    name = "OnlineHDWatch"
    domains = ['movieshdwatch.net']
    sources = []   
    def __init__(self):
        self.base_link = 'http://www.movieshdwatch.net'
        self.sources = []  
        
    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())                                                                                                                           #(movie name keeping spaces removing excess characters)

            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+')) 
            print start_url
            headers = {'User_Agent':User_Agent}
            html = requests.post(start_url).content
            print html
            match = re.compile('<div class="boxinfo".+?href="(.+?)".+?<h2>(.+?)</h2>.+?class="year">(.+?)</span>',re.DOTALL).findall(html)
            for url,name,date in match:
                clean_name=name.split(' (')[0]
                if not year in date:
                    continue
                if clean_title(title) == clean_title(clean_name):
                
                    html2 = requests.get(url).content
                    frames = re.findall('<iframe.+?src="(.+?)"',html2)
                    try: quality = re.findall('<span class="calidad2">(.+?)</span>',html2)[0]
                    except: quality = 'HD'
                    for playlink in frames:
                        source = re.findall('//(.+?)/',str(playlink))[0]
                        if 'o' in str(source) and 'load' in str(source):
                            self.sources.append({'source': source,'quality': quality,'scraper': self.name,'url': playlink,'direct': False})
            return self.sources
        except Exception as e:
            
            return []                           

    #scrape_movie('the mummy', '2017', debrid=False)

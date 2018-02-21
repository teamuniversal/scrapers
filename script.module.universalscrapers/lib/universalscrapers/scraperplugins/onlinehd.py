import re
import requests
import xbmc
from ..scraper import Scraper
from ..common import clean_search, clean_title


class OnlineHDWatch(Scraper):
    name = "OnlineHDWatch"
    domains = ['movieshdwatch.net']
    sources = []   
    def __init__(self):
        self.base_link = 'http://www.movieshdwatch.net'
        self.search_link = '/?s='
        self.sources = []  
    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_url = self.base_link+self.search_link+clean_search(title).replace(' ','+')+'+'+year
            html = requests.post(start_url).content
            match = re.findall('<div class="boxinfo">.+?<a href="(.+?)">.+?<span.+?>(.+?)</span>',html,re.DOTALL)
            for url,name in match:
                clean_name,clean_year = re.findall('(.+?)20(.+?) ',str(name))[0]
                clean_year = '20'+clean_year.replace(')','')
                clean_name = clean_title(clean_name).replace('(','')
                if 'full' in str(name).lower().replace(' ','') and 'movie' in str(name).lower().replace(' ',''):
                    if year==clean_year and clean_title(title) == clean_name:
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

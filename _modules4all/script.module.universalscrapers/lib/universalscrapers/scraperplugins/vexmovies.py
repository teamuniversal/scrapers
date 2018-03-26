import requests
import re
####### kodi #########
import xbmc
import xbmcaddon
import time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
####### idle #########
# from nanscrapers.common import clean_title,clean_search,random_agent

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")
  
class vexmovies(Scraper):
    domains = ['http://vexmovies.org']
    name = "VexMovies"
    sources = []

    def __init__(self):
        self.base_link = 'http://vexmovies.org'
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content
            match = re.compile('id="mt-.+?href="(.+?)">.+?alt="(.+?)".+?<span class="year">(.+?)</span>.+?class="calidad2">(.+?)</span>',re.DOTALL).findall(html)
            for item_url,name,release,qual in match:
                if year == release:
                    if clean_title(search_id).lower() == clean_title(name).lower():                              
                        self.get_source(item_url,qual)                                      
            return self.sources
        except Exception, argument:        
             if dev_log == 'true':
                 error_log(self.name,'Check Search')

    def get_source(self,item_url,qual):
        try:
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(item_url,headers=headers,timeout=5).content           

            Endlinks = re.compile('class="entry-content">.+?<iframe src="(.+?)".+?</iframe>',re.DOTALL).findall(OPEN)  
            for link in Endlinks:
            	consistant = requests.get(link,headers=headers,timeout=5).content
            	final_links = re.compile('src&quot;:&quot;(.+?)&quot',re.DOTALL).findall(consistant)
            	for links in final_links:
            		irl= 'irl-'
            		gool = 'googleusercontent'
            		if irl not in links:
            			if gool not in links:
            				links = links.replace('\\','')
			                host = links.split('//')[1].replace('www.','')
			                hostname = host.split('/')[0].split('.')[0].title()
			                self.sources.append({'source': hostname, 'quality': qual, 'scraper': self.name, 'url': links,'direct': False})   
                        if dev_log=='true':
                            end_time = time.time() - self.start_time
                            send_log(self.name,end_time,count)
        except:
            pass

# vexmovies().scrape_movie('Justice League', '2017','')

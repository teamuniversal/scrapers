import requests
import re, base64
import xbmc
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent

  
class housemovie(Scraper):
    domains = ['https://housemovie.to/']
    name = "Housemovies"
    sources = []

    def __init__(self):
        self.base_link = 'https://housemovie.to'


    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())                                     # use 'clean_search' to get clean title 
                                                                                        #(movie name keeping spaces removing excess characters)
            start_url = '%s/search?q=%s' %(self.base_link,search_id.replace(' ','+'))      # construct search url attributes using site url
#            print '::::::::::::: START URL '+start_url                                  # print to log to confirm 
            
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content            # open start_url
            match = re.compile('<span class="is_dislike">.+?<a href="(.+?)" class="fig_holder">.+?<div class="cover-label">.+?<spa.+?>(.+?)</span>.+?<span class="item_name">(.+?)</span>.+?<span class="item_ganre">(.+?),',re.DOTALL).findall(html)
            for url, quality, name, year_check in match:
                if clean_title(search_id).lower() == clean_title(name).lower():     # confirm name use 'clean_title' this will remove all unwanted
                    if year_check == year:
                        url = self.base_link+url
                        if not 'coming soon' in quality.lower():
                            self.get_source(url, quality)                                       # send url to next stage
            return self.sources
        except Exception as e:
            print e
            pass
            return[]

            
    def get_source(self, item_url, quality):
        try:
            headers={'User-Agent':random_agent()}
            html = requests.get(item_url,headers=headers,timeout=5).content             # open page passed
            try:
                mainlink = re.findall('<iframe src="(.+?)"',html).findall(OPEN)[0]
                source = re.findall('//(.+?)/',str(mainlink))[0]
                self.sources.append({'source': source, 'quality': quality, 'scraper': self.name, 'url': link,'direct': False}) #this line will depend what sent
            except:
                pass
            match_links = re.findall('data-link="(.+?)" rel="nofollow">(.+?)</a>',html)
            for link,name in match_links:
                link = base64.decodestring(link)
                link = re.findall('"link":"(.+?)"',str(link.replace('\\','')))[0]
                source = re.findall('//(.+?)/',str(link))[0]
                self.sources.append({'source': source, 'quality': quality, 'scraper': self.name, 'url': link,'direct': False}) #this line will depend what sent     
        except Exception as e:
            print e

#housemovie().scrape_movie('logan','2017','')
# you will need to regex/split or rename to get host name if required from link unless available on page it self 

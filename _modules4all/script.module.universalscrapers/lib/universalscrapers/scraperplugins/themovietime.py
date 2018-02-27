import requests
import resolveurl
import re
import xbmc,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent

  
class themovietime(Scraper):
    domains = ['http://themovietime.net']
    name = "The Movie Time"
    sources = []

    def __init__(self):
        self.base_link = 'http://themovietime.net'
        self.start_time = time.time()                                                   # start the timer for the script


    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())                                     # use 'clean_search' to get clean title 
                                                                                        #(movie name keeping spaces removing excess characters)

            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))         # construct search url attributes using site url
            #print '::::::::::::: START URL '+start_url                                  # print to log to confirm 
            
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content            # open start_url
            
            match = re.compile('<div class="title">.+?href="(.+?)">(.+?)</a>.+?class="year">(.+?)</span>',re.DOTALL).findall(html) # Regex info on results page
            for item_url, name, year in match:
                #print 'item_url>>>>>>>>>>>>>> '+item_url                                # use print statments to confirm grabs check log
                #print 'name>>>>>>>>>>>>>> '+name
                #print  'year>>>>>>>>>>>>>>'+year
                if year in year:                                                        # confirm year if available in results sometines in name grab/or regex elsewhere
                    
                    if clean_title(search_id).lower() == clean_title(name).lower():     # confirm name use 'clean_title' this will remove all unwanted
                                                                                        # incuding spaces to get both in same format to match if correct
                        print 'Send this URL> ' + item_url                              # confirm in log correct url(s) sent to get_source
                        self.get_source(item_url)                                       # send url to next stage
            return self.sources
        except:
            pass
            return[]

            
    def get_source(self,item_url):
        try:
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(item_url,headers=headers,timeout=5).content             # open page passed

            Endlinks = re.compile('<iframe class=.+?src="(.+?)"',re.DOTALL).findall(OPEN)      # regex to links
            for link in Endlinks:
                if 'openload' in link:
                    try:
                        headers = {'User_Agent':User_Agent}
                        get_res=requests.get(link,headers=headers,timeout=5).content
                        rez = re.compile('',re.DOTALL).findall(get_res)[0]
                        if '1080' in rez:
                            qual ='1080p'
                        elif '720p' in rez:
                            qual='720p'
                        else:
                            qual='DVD'
                    except: qual='DVD'
                    self.sources.append({'source': 'Openload','quality': qual,'scraper': self.name,'url': link,'direct': False})

                else:
                    if urlresolver.HostedMediaFile(link):
                        host = link.split('//')[1].replace('www.','')
                        host = host.split('/')[0].split('.')[0].title()
                        self.sources.append({'source': host,'quality': 'DVD','scraper': self.name,'url': link,'direct': False})
        except:
            pass

                        

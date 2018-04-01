import requests
import re
import base64
import xbmc
import xbmcaddon
import time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class alluno(Scraper):
    domains = ['https://www.alluc.uno']
    name = "alluno"
    sources = []

    def __init__(self):
        self.base_link = 'https://www.alluc.uno'
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())                       
                                                                                 

            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+')+'+'+year)         
            print '::::::::::::: START URL '+start_url                               

            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content          
            match = re.compile('class="resblock">.+?href=\'(.+?)\'.+?class="masterTooltip.+?title="(.+?)".+?href=".+?">(.+?)</a>.+?</div></div>',re.DOTALL).findall(html) # Regex info on results page
            for item_url,name,host in match:
                # print 'item_url>>>>>>>>>>>>>> '+item_url                              
                # print 'name>>>>>>>>>>>>>> '+name

                if year in name:
                    # print 'yes'                                                        
                    if clean_title(search_id).lower() in clean_title(name).lower():     
                                                                                       
                        print 'Send this URL> ' + item_url                              
                        self.get_source(item_url,host)                                      
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
               

            
    def get_source(self,item_url,host):
        try:
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(item_url,headers=headers,timeout=5).content       

            bsix = re.compile('class="media"><button id="watchbutton".+?data-src="(.+?)".+?</iframe> </div></div></div>',re.DOTALL).findall(OPEN) 
            count = 0
            for bsix4 in bsix:
                Endlinks = base64.b64decode(bsix4)
                if '1080' in item_url:
                    label = '1080p'
                elif '720' in item_url:
                    label = '720p'
                else:
                    label = 'SD'
                # print Endlinks
                # print label    
                host = Endlinks.split('//')[1].replace('www.','')
                hostname = host.split('/')[0].split('.')[0].title()
                count +=1
            self.sources.append({'source': hostname, 'quality': label, 'scraper': self.name, 'url': Endlinks,'direct': False})
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')

# alluno().scrape_movie('justice league', '2017','')

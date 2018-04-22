## cant get to open odd ? petok token maybe 

import requests,re,base64,xbmc
import xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,error_log,send_log
from universalscrapers.modules import cfscrape
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class alluno(Scraper):
    domains = ['https://www.alluc.uno']
    name = "alluno"
    sources = []

    def __init__(self):
        self.base_link = 'https://www.alluc.uno'
        self.scraper = cfscrape.create_scraper()
        if dev_log=='true':
            self.start_time = time.time()
        self.count = 0

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())                       
                                                                                 

            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+')+'+'+year)         
            print '::::::::::::: START URL '+start_url                               

            headers={'User-Agent':random_agent()}
            html = self.scraper.get(start_url,headers=headers,verify=False).content    
            print html
            match = re.compile('class="resblock".+?class="masterTooltip.+?href="(.+?)" title="(.+?)"',re.DOTALL).findall(html)
            for item_url,name in match:
                # print 'item_url>>>>>>>>>>>>>> '+item_url                              
                # print 'name>>>>>>>>>>>>>> '+name

                if year in name:
                    # print 'yes'                                                        
                    if clean_title(search_id).lower() in clean_title(name).lower():     
                                                                                       
                        print 'Send this URL> ' + item_url                              
                        self.get_source(item_url) 
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,self.count)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
               

            
    def get_source(self,item_url,host):
        try:
            headers={'User-Agent':random_agent()}
            OPEN = self.scraper.get(item_url,headers=headers,timeout=5).content       

            bsix = re.compile('class="media"><button id="watchbutton".+?data-src="(.+?)".+?</iframe> </div></div></div>',re.DOTALL).findall(OPEN) 

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
                self.count +=1
                self.sources.append({'source': hostname, 'quality': label, 'scraper': self.name, 'url': Endlinks,'direct': False})
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Source')

# alluno().scrape_movie('justice league', '2017','')

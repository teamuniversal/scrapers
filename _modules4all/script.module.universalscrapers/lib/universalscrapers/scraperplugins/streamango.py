#checked 3/9/2108
import requests
import urlparse
import re
import resolveurl as urlresolver
import xbmc,xbmcaddon,time
import base64
from universalscrapers.modules import cfscrape
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class streamango(Scraper):
    domains = ['streamango.stream']
    name = "Streamango Stream"
    sources = []

    def __init__(self):
        self.base_link = 'https://streamango.stream/'
        
    def scrape_movie(self, title, year, imdb, debrid = False):
        try:

            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                      
            start_url = '%s?s=%s' %(self.base_link,search_id.replace(' ','+'))         
            #print 'scraperchk - scrape_movie - start_url:  ' + start_url                                  
            headers={'User-Agent':random_agent()}
            scraper = cfscrape.create_scraper()
            html = scraper.get(start_url,headers=headers,timeout=5).content            
            match = re.compile('<li class="TPostMv".+?class="TPMvCn">.+?<a href="(.+?)"><div class="Title">(.+?)</div></a>.+?class="Date">(.+?)</span><span class="Qlty">(.+?)</span>',re.DOTALL).findall(html) 
            for item_url, name, date, res in match:
                #print 'scraperchk - scrape_movie - name: '+name+ ' '+date
                #print 'scraperchk - scrape_movie - item_url: '+item_url+'   '+res
                if year in date:                                                           
                    if clean_title(search_id).lower() == clean_title(name).lower():                                                                    
                        #print 'scraperchk - scrape_movie - Send this URL: ' + item_url                             
                        self.get_source(item_url,title,year,start_time,res)                                      
            return self.sources
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument) 
 

    def get_source(self,item_url,title,year,start_time,res):
        try:
            #print 'PASSEDURL >>>>>>'+item_url
            count = 0
            scraper = cfscrape.create_scraper()
            headers={'User-Agent':random_agent()}
            OPEN = scraper.get(item_url,headers=headers,timeout=5).content
            Endlinks = re.compile('TrvideoFirst\">(.+?)</div>',re.DOTALL).findall(OPEN)
            #print 'scraperchk - scrape_movie - EndLinks: '+str(Endlinks)
            for link2 in Endlinks:
                #print 'scraperchk - scrape_movie - link: '+str(link2)        
                link1=base64.b64decode(link2)
                #print link1+'decoded?????????????????????????????????????????'
                Endlink =link1.split('src=')[1].split('allowfullscreen')[0].replace('"','').rstrip()
                #print Endlink +'<<<<<<<<<<<<<<<<endlink>>>>>>>>>>>>>>'
                if 'openlinks' in Endlink:
                    headers= {'User-Agent':random_agent()}
                    OPEN = requests.get(Endlink,headers=headers,timeout=5,allow_redirects=True).content
                    finalurl = re.compile('url\" content="(.+?)">',re.DOTALL).findall(OPEN)
                    for link in finalurl:
                        #print '===================================='+link
                        count+=1
                        host = link.split('//')[1].replace('www.','')
                        host = host.split('/')[0].split('.')[0].title()
                        self.sources.append({'source':host, 'quality':res, 'scraper':self.name, 'url':link, 'direct':False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return[]
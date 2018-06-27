import requests
import urlparse
import re
import resolveurl as urlresolver
import xbmc
import xbmcaddon,time
import base64
from ..jsunpack import unpack
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class cenflix(Scraper):
    domains = ['https://www.cenflix.co']
    name = "CenFlix"
    sources = []

    def __init__(self):
        self.base_link = 'https://www.cenflix.co'


    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                      
                                                                                        

            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))         
            #print 'scrapercheck - scrape_movie - start_url:  ' + start_url                                  
            
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content            
            
            match = re.compile('class="result-item".+?href="(.+?)".+?alt="(.+?)".+?class="year">(.+?)</span>',re.DOTALL).findall(html) 
            for item_url, name,rel in match:
                #print 'scrapercheck - scrape_movie - name: '+name + '   '+rel
                #print 'scrapercheck - scrape_movie - item_url: '+item_url                                                           
                if clean_title(search_id).lower() == clean_title(name).lower():
                    if rel == year:    
                                                                                        
                        #print 'scrapercheck - scrape_movie - Send this URL: ' + item_url                             
                        self.get_source(item_url,title,year,start_time)                                      
            return self.sources
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument) 

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_time = time.time()
            seaepi_chk = '%sx%s' %(season,episode)
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=10).content
            #print html
            match = re.compile('class="result-item".+?href="(.+?)".+?alt="(.+?)"',re.DOTALL).findall(html)
            for tvshow_url, title in match:
                #print tvshow_url +' '+ title
                headers = {'User-Agent':random_agent()}
                html = requests.get(tvshow_url,headers=headers,timeout=10).content
                match = re.compile('class="imagen"><a href="(.+?)"',re.DOTALL).findall(html)
                for sea_ep in match:
                    #print sea_ep+'<<<<'
                    if not seaepi_chk in sea_ep:
                        continue
                    #print 'PASSED OK ??????'+ sea_ep    
                    headers={'User-Agent':random_agent()}
                    html1 = requests.get(sea_ep,headers=headers,timeout=10).content
                    match1 = re.compile('class="play-box-iframe fixidtab".+?src="(.+?)"',re.DOTALL).findall(html1)
                    for link in match1:
                        #print link +'::::::::::::::::::::::'
                        if urlresolver.HostedMediaFile(link):
                            host = link.split('//')[1].replace('www.','')
                            host = host.split('/')[0].split('.')[0].title()
                            self.sources.append({'source':host, 'quality':'DVD', 'scraper':self.name, 'url':link, 'direct':False})
                        else:
                            if 'sibeol' in link:
                                #print link + 'SIBEOL LINK??????????????'
                                get_link_page = requests.get(link,headers=headers,timeout=10).content
                                #print get_link_page + 'UNJUICE?????????????????'
                                juicify = re.compile('>JuicyCodes.Run\("(.+?)\)\;\<',re.DOTALL).findall(get_link_page)
                                for juicified in juicify:
                                    dejuice5= juicified.replace('"+"','')
                                    dejuice4 = base64.b64decode(dejuice5)
                                    dejuice3 = unpack(dejuice4)
                                    #for dejuice in dejuice3:
                                    Endlinks2 = re.compile('"file":"(.+?)","label":"(.+?)","type"',re.DOTALL).findall(dejuice3)
                                    for link, qual in Endlinks2:
                                        print link 
                                        host = link.split('//')[1].replace('www.','')
                                        host = host.split('/')[0].split('.')[0].title()
                                        self.sources.append({'source':host, 'quality':qual, 'scraper':self.name, 'url':link, 'direct':True})
                return self.sources
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument) 




    def get_source(self,item_url,title,year,start_time):
        try:
            #print 'PASSEDURL >>>>>>'+item_url
            count = 0
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(item_url,headers=headers,timeout=10).content
            Endlinks1 = re.compile('<iframe class.+?src="(.+?)"',re.DOTALL).findall(OPEN)
            for link in Endlinks1:     
                if urlresolver.HostedMediaFile(link):
                    count+=1
                    host = link.split('//')[1].replace('www.','')
                    host = host.split('/')[0].split('.')[0].title()
                    self.sources.append({'source':host, 'quality':'DVD', 'scraper':self.name, 'url':link, 'direct':False})
                else:
                    if 'sibeol' in link:
                                #print link + 'SIBEOL LINK??????????????'
                                get_link_page = requests.get(link,headers=headers,timeout=10).content
                                #print get_link_page + 'UNJUICE?????????????????'
                                juicify = re.compile('>JuicyCodes.Run\("(.+?)\)\;\<',re.DOTALL).findall(get_link_page)
                                for juicified in juicify:
                                    dejuice5= juicified.replace('"+"','')
                                    dejuice4 = base64.b64decode(dejuice5)
                                    dejuice3 = unpack(dejuice4)
                                    #for dejuice in dejuice3:
                                    Endlinks2 = re.compile('"file":"(.+?)","label":"(.+?)","type"',re.DOTALL).findall(dejuice3)
                                    for link, qual in Endlinks2:
                                        #print link 
                                        host = link.split('//')[1].replace('www.','')
                                        host = host.split('/')[0].split('.')[0].title()
                                        self.sources.append({'source':host, 'quality':qual, 'scraper':self.name, 'url':link, 'direct':True})


            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return[]
import requests
import urlparse
import re
import resolveurl as urlresolver
import xbmc,xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class hdvix(Scraper):
    domains = ['hdvix.com']
    name = "HDvix"
    sources = []

    def __init__(self):
        self.base_link = 'https://hdvix.com'
        
    def scrape_movie(self, title, year, imdb, debrid = False):
        try:

            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                      
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))         
            #print 'scraperchk - scrape_movie - start_url:  ' + start_url                                  
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content            
            match = re.compile('class="thumb".+?title="(.+?)".+?href="(.+?)">',re.DOTALL).findall(html) 
            for name, item_url in match:
                print 'scraperchk - scrape_movie - name: '+name
                #print 'scraperchk - scrape_movie - item_url: '+item_url
                if year in name:                                                           
                    if clean_title(search_id).lower() == clean_title(name).lower():                                                                    
                        #print 'scraperchk - scrape_movie - Send this URL: ' + item_url                             
                        self.get_source(item_url,title,year,start_time)                                      
            return self.sources
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument) 

    # def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
    #     try:
    #         start_time = time.time()
    #         season_chk = '-season-%s' %(season)
    #         #print season_chk
    #         search_id = clean_search(title.lower())
    #         start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
    #         headers={'User-Agent':random_agent()}
    #         html = requests.get(start_url,headers=headers,timeout=5).content
    #         match = re.compile('class="ml-item".+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
    #         for season_url, title in match:
    #             #print season_url
    #             if not season_chk in season_url:
    #                 continue
    #             #print 'PASSED season URL### ' +season_url
    #             episode_grab = 'Season %s Episode %s ' %(season,episode)

    #             item_url = self.base_link+season_url+'/watching.html'
    #             html=requests.get(item_url, headers=headers, timeout=5).content
    #             match = re.compile('<a title="(.+?)" player-data="(.+?)"',re.DOTALL).findall(html)
    #             for epi, link in match:
    #                 epi = epi.split('-')[1].split('-')[0]

    #                 if not clean_title(epi).lower() == clean_title(episode_grab).lower():
    #                     continue
    #                 #print 'Passed episode > '+epi
    #                 #if link.startswith('://vidnode.net/'):
    #                     #link = link.replace('://vidnode.net/','https://vidnode.net/')
    #                 if link.startswith('//vidnode.net/'):
    #                     link = link.replace('//vidnode.net/','https://vidnode.net/')
    #                 #print 'matched link>>> ' + link
    #                 host = link.split('//')[1].replace('www.','')
    #                 host = host.split('/')[0].split('.')[0].title()

    #                 self.sources.append({'source':host, 'quality':'SD', 'scraper':self.name, 'url':link, 'direct':False})
    #             return self.sources
    #     except Exception, argument:
    #         if dev_log=='true':
    #             error_log(self.name,argument) 



    


    def get_source(self,item_url,title,year,start_time):
        try:
            #print 'PASSEDURL >>>>>>'+item_url
            count = 0
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(item_url,headers=headers,timeout=5).content
            #print OPEN
            Endlinks1 = re.compile('class="screen fluid-width-video-wrapper">.+?src="(.+?)"',re.DOTALL).findall(OPEN)
            #print 'scraperchk - scrape_movie - EndLinks: '+str(Endlinks1)
            for nxpg in Endlinks1:       
                headers={'User-Agent':random_agent()}
                OPEN = requests.get(nxpg,headers=headers,timeout=5).content
                BLOCK = re.compile('class="menuPlayer">(.+?)</ul>',re.DOTALL).findall(OPEN)
                #print BLOCK
                Endlinks = re.compile('href="(.+?)"',re.DOTALL).findall(str(BLOCK))
                #print Endlinks
                for link in Endlinks:
                    #print link+'<<<<<<<<<<<<<<<<<<<<<<<<<<'
                    if '1080' in link:
                        qual = '1080p'
                    if '720' in link:
                        qual = '720p'
                    else:
                        qual = 'SD'
                        count+=1
                        host = link.split('//')[1].replace('www.','')
                        host = host.split('/')[0].split('.')[0].title()
                        self.sources.append({'source':host, 'quality':qual, 'scraper':self.name, 'url':link, 'direct':False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return[]
import requests, resolveurl
import re
import xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")
#user_agent='Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
# same site as hollymoviehd

class novamovie(Scraper):
    domains = ['https://www.novamovie.net/']
    name = "HollyMovieHD1"
    sources = []

    def __init__(self):
        self.base_link = 'https://www.novamovie.net/'
        if dev_log=='true':
            self.start_time = time.time()                                                   

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())                                      
                                                                                        
            start_url = '%s?mysrc=search&s=%s' %(self.base_link,search_id.replace(' ','+'))         
            #print '::::::::::::: START URL '+start_url                                   
            
            #headers={'User-Agent':user_agent, referrer:self.base_link}
            html = requests.get(start_url,timeout=5).content            
            #print html
            match = re.compile('class="ml-item".+?href="(.+?)".+?oldtitle="(.+?)"',re.DOTALL).findall(html) 
            for item_url, name in match:
                print 'item_url>>>>>>>>>>>>>> '+item_url                                
                print 'name>>>>>>>>>>>>>> '+name
                if year in name:                                                        
                    if clean_title(search_id).lower().replace(' ','') == clean_search(name.lower()).split(year)[0].replace(' ',''):
                        #print 'Send this URL> ' + item_url                              
                        self.get_source(item_url)                                       
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')

            
    def get_source(self,item_url):
        try:
            OPEN = requests.get(item_url,timeout=5).content
            #print OPEN
            holder = re.compile('<iframe.+?src="(.+?)"',re.DOTALL).findall(OPEN)
            count = 0
            for sources in holder:
                print sources
                if sources.startswith('//'):
                    sources = 'https:' + sources
                #print 'embfile>> '+sources
            
                #headers={'User-Agent':random_agent()}

                Page = requests.get(sources,timeout=5).content
                #print 'page1234'+Page
                link_list = []
                Endlinks = re.compile("<iframe src=['\"](.+?)['\"]",re.DOTALL).findall(Page)
                for links in Endlinks:
                    link_list.append(links)
                Endlinks1= re.compile('file:"(.+?)"',re.DOTALL).findall(Page)
                for links in Endlinks1:
                    link_list.append(links)
                for link in link_list:
                #for link in Endlinks:
                    print 'TRY ME > '+link
                    if 'openload' in link:
                        try:
                            headers = {'User_Agent':random_agent()}
                            get_res=requests.get(link,timeout=5).content
                            rez = re.compile('description" content="(.+?)"',re.DOTALL).findall(get_res)[0]
                            if '1080p' in rez:
                                qual = '1080p'
                            elif '720p' in rez:
                                qual='720p'
                            else:
                                qual='SD'
                        except: qual='SD'
                        count +=1 
                        self.sources.append({'source': 'Openload','quality': qual,'scraper': self.name,'url': link,'direct': False})
                    
                    else:
                        try:
                            Endlinks1= re.compile('file:"(.+?)"',re.DOTALL).findall(Page)
                            for link1 in Endlinks1:
                                #print link1+'<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
                                host = link.split('//')[1].replace('www.','')
                                host = host.split('/')[0].split('.')[0].title()
                                count +=1
                                self.sources.append({'source': host, 'quality': 'SD', 'scraper': self.name, 'url': link,'direct': False})
             
                        except:pass
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)                                  
        except:
            pass
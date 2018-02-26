import requests,re,time,xbmcaddon
from ..scraper import Scraper
from universalscrapers.modules import cfscrape
from ..common import clean_title,clean_search,random_agent,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


User_Agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4'  

class ChillnFlix(Scraper):
    domains = ['https://chillnflix.to']
    name = "ChillnFlix"
    sources = []

    def __init__(self):
        self.base_link = 'https://chillnflix.to'
        self.scraper = cfscrape.create_scraper()
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            headers = {'User_Agent':User_Agent}
            html = self.scraper.get(start_url,headers=headers,timeout=10).content
            match = re.compile('class="ml-item".+?href="(.+?)".+?title="(.+?)".+?mli-quality">(.+?)</span>.+?</span>',re.DOTALL).findall(html)
            for item_url,name,qaul in match:
                watch = '?action=watching'
                item_url = item_url+watch
                if not year in item_url:
                    continue
                if not clean_title(search_id).lower() == clean_title(name).lower():
                    continue
                self.get_source(item_url,qaul)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

            
    def get_source(self,item_url,qaul):
        try:
            OPEN = self.scraper.get(item_url,timeout=10).content

            block1 = re.compile('<iframe src="(.+?)<div id="bar-player">',re.DOTALL).findall(OPEN)

            Endlinks = re.compile('<iframe.+?src=.+?"(.+?)"><.+?/iframe>',re.DOTALL).findall(str(block1))
            count = 0
            for link in Endlinks:
                
                link = link.replace('\\','')
                link = link.replace('" allowfullscreen="true" frameborder="0" marginwidth="0" marginheight="0" scrolling="no','')
                link = 'http:'+link
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].lower()
                host = host.split('.')[0]
                print '>>>>>>>>>>>>'+link
                count +=1
                # xbmc.log('************ LOG THIS '+repr(link),xbmc.LOGNOTICE)
                self.sources.append({'source': host, 'quality': qaul, 'scraper': self.name, 'url': link,'direct': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)
        except:
            pass

  
    
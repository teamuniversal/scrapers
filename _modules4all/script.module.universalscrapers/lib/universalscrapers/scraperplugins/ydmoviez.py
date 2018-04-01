import requests,re,time,xbmcaddon
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class ydmoviez(Scraper):
    domains = ['http://ydmoviez.com/']
    name = "ydmoviez"
    sources = []

    def __init__(self):
        self.base_link = 'http://ydmoviez.com/'
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s?s=%s' %(self.base_link,search_id.replace(' ','+'))
            # xbmc.log('************ LOG THIS '+repr(start_url),xbmc.LOGNOTICE)
            html = requests.get(start_url,timeout=10).content
            #print html
            match = re.compile('class="result-item">.+?href="(.+?)".+?alt="(.+?)".+?class="year">(.+?)</span>.+?<p>.+?</article>',re.DOTALL).findall(html)
            for item_url,name,yrs in match:
                #item_url = 'http:%s' % (item_url)
                if not year in yrs:
                    continue
                if not clean_title(search_id).lower() == clean_title(name).lower():
                    continue
                self.get_source(item_url)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

            
    def get_source(self,item_url):
        # print item_url
        try:
            OPEN = requests.get(item_url,timeout=10).content
            Endlinks = re.compile('class="metaframe.+?src="(.+?)"\s*frameborder',re.DOTALL).findall(OPEN)
            Rez = re.compile('class="qualityx">(.+?)</span>.+?class="qualityx">.+?class="qualityxx">',re.DOTALL).findall(OPEN)
            count = 0
            for link in Endlinks:
                #link = 'http:%s' % (link)
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].lower()
                host = host.split('.')[0]
                count +=1
                for rez in Rez:
                #print link
                	self.sources.append({'source': host, 'quality': rez, 'scraper': self.name, 'url': link,'direct': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)
        except:
            pass
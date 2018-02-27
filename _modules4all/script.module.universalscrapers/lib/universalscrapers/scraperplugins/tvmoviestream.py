import requests,re,time,xbmcaddon
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class tvmoviestream(Scraper):
    domains = ['https://tvmoviestream.me/']
    name = "TvMovieStream"
    sources = []

    def __init__(self):
        self.base_link = 'https://tvmoviestream.me/'
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s?s=%s' %(self.base_link,search_id.replace(' ','+'))
            #print start_url
            #xbmc.log('************ LOG THIS '+repr(start_url),xbmc.LOGNOTICE)
            html = requests.get(start_url).content
            #print html
            match = re.compile('<div class="result-item">.+?href="(.+?)".+?alt="(.+?)".+?<span class="year">(.+?)</span>',re.DOTALL).findall(html)
            for item_url,name,yrs in match:
                #print item_url
                #print name
                ##print yrs
                if year == yrs:
                    if clean_title(search_id).lower() == clean_title(name).lower():
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
            match1 = re.compile('<iframe.+?src="(.+?)"',re.DOTALL).findall(OPEN)
            #block = re.compile('name="permalink" value=(.+?)class="report-video"',re.DOTALL).findall(html)
            #match = re.compile('<iframe \s*class="metaframe\s*rptss"\s*src="(.+?)".+?</iframe>',re.DOTALL).findall(str(block))
            for link in match1:
            	if 'youtube' not in link:
                #xbmc.log('************ LOG THIS '+repr(link),xbmc.LOGNOTICE)
                	host = link.split('//')[1].replace('www.','')
                	host = host.split('/')[0].lower()
                	host = host.split('.')[0] 
                	self.sources.append({'source': host, 'quality': 'sd', 'scraper': self.name, 'url': link,'direct': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)
        except:
            pass

#tvmoviestream().scrape_movie('fifty shades freed', '2018','')
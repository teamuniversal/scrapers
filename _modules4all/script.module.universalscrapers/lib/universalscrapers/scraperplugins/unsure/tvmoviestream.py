import requests,re,time,xbmcaddon
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class tvmoviestream(Scraper):
    domains = ['https://tvmoviestream.me/']
    name = "TvMovieStream"
    sources = []

    def __init__(self):
        self.base_link = 'https://tvmoviestream.me/'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            search_id = clean_search(title.lower())
            start_url = '%s?s=%s' %(self.base_link,search_id.replace(' ','+'))
            print start_url

            headers = {'User_Agent':User_Agent}
            html = requests.get(start_url,headers=headers, timeout=5).content
            #print html
            match = re.compile('<div class="result-item">.+?href="(.+?)".+?alt="(.+?)".+?class="year">(.+?)</span>',re.DOTALL).findall(html)
            for item_url,name,yrs in match:
                #print item_url
                #print name
                ##print yrs
                if clean_title(search_id).lower() == clean_title(name).lower():
                    if year in yrs:
                        print 'pass me '+item_url
                        self.get_source(item_url,title,year,'','',start_time)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

            
    def get_source(self,item_url, title, year, season, episode, start_time):
        print item_url
        try:
            headers = {'User_Agent':User_Agent}
            OPEN = requests.get(item_url,headers=headers,timeout=10).content
            print OPEN
            match = re.compile('<iframe.+?src="(.+?)"',re.DOTALL).findall(OPEN)
            for link in match:
            	if 'youtube' not in link:

                	host = link.split('//')[1].replace('www.','')
                	host = host.split('/')[0].lower()
                	host = host.split('.')[0] 
                	self.sources.append({'source': host, 'quality': 'SD', 'scraper': self.name, 'url': link,'direct': False})

            match2 = re.compile('href="(https://tvmoviestream.me/links/.+?)"',re.DOTALL).findall(OPEN)
            for altlink in match2:
                print altlink
                headers = {'User-Agent': User_Agent}
                r = requests.get(altlink,headers=headers,allow_redirects=False)
                final_url = r.headers['location']
                
            	host = final_url.split('//')[1].replace('www.','')
                host = host.split('/')[0].lower()
                host = host.split('.')[0] 
                if '1080' in final_url:
                    res = '1080p'
                elif '720' in final_url:
                    res = '720p'
                else:
                    res='SD'
                self.sources.append({'source': host, 'quality': res, 'scraper': self.name, 'url': final_url,'direct': False})

        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

#tvmoviestream().scrape_movie('fifty shades freed', '2018','')
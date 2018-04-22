import requests,re,time,xbmcaddon
import base64,resolveurl
from ..scraper import Scraper
from universalscrapers.modules import cfscrape
from ..common import clean_title,clean_search,random_agent,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")  

class extramovies(Scraper):
    domains = ['http://extramovies.cc/']
    name = "extramovies"
    sources = []

    def __init__(self):
        self.base_link = 'http://extramovies.cc'
        #self.scraper = cfscrape.create_scraper()
        self.sources=[]

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            search_id = clean_search(title.lower()) 
            start_url = self.base_link + '/?s=' +search_id.replace(' ','+')
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content 
            match = re.compile('class="thumbnail">.+?href="(.+?)" title="(.+?)".+?class="rdate">(.+?)</span>.+?</article>',re.DOTALL).findall(html) # Regex info on results page
            for item_url, name ,release in match:
                release = release.strip()
                if year == release:
                    if year in release:
                        self.get_source(item_url,title,year,'','',start_time)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

            
    def get_source(self,item_url,title,year,season,episode,start_time):
        try:
            #print 'CHKMYURL >'+url
            rez = item_url
            if '1080' in rez:
                res = '1080p'
            elif '720' in rez:
                res = '720p'
            else: 
                res = 'DVD'
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(item_url,headers=headers,timeout=10).content
            #print OPEN
            Regex = re.compile('href="/download.php.+?link=(.+?)"',re.DOTALL).findall(OPEN)
            count = 0
            for link in Regex:
                #print link
                try:
                    link = base64.b64decode(link)
                except:pass
                if not resolveurl.HostedMediaFile(link).valid_url(): 
                    continue
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                if 'Www' not in host:
                    count +=1
                    print link
                    if 'google' in link:
                        continue
                    #print ' ##finalurl## %s | >%s<' %(self.name,link)
                    self.sources.append({'source': host, 'quality': res, 'scraper': self.name, 'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year,season,episode)
        except:
            pass
# extramovies().scrape_movie('justice league', '2017','')
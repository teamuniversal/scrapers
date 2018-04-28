import re,requests
import resolveurl as urlresolver
import xbmcaddon,time  
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

class WatchFrees(Scraper):
    domains = ['watchfrees.com']
    name = "watchfrees"
    sources = []

    def __init__(self):
        self.base_link = 'https://watchfree.movie' #'https://watchfrees.com'


    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_time = time.time()
            ep_string = '-season-%s-episode-%s-' %(season, episode)
            search_id = clean_search(title.lower())
            start_url = '%s/search.html?keyword=%s' %(self.base_link,search_id.replace(' ','+'))
            print start_url
            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
            print html
            match = re.compile('<figure>.+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
            for url,name in match:
                if clean_title(title).lower() in clean_title(name).lower():
                    season_url = self.base_link + url
                    #print 'shows >'+season_url
                    if 'Season '+season in name:
                        #print 'correct season shows >'+season_url
                        headers={'User-Agent':User_Agent}
                        html2 = requests.get(season_url,headers=headers,timeout=10).content
                        ulist = re.compile('<ul>(.+?)</ul>',re.DOTALL).findall(html2)
                        match2 = re.compile('<a href="(.+?)"',re.DOTALL).findall(str(ulist))
                        for epi_url in match2:
                            if not ep_string in epi_url:
                                continue
                            url = self.base_link+epi_url
                            #print 'pass watchepisode url ' +url
                            self.get_source(url,title,year,season,episode,start_time)

            return self.sources
                                        
        except:
            pass
            return []                           

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            search_id = clean_search(title.lower())
            start_url = '%s/search.html?keyword=%s' %(self.base_link,search_id.replace(' ','+'))
            print start_url
            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
            print html
            match = re.compile('<figure>.+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
            for url,name in match:
                name=name.replace('Movie','')
                if clean_title(title).lower() == clean_title(name).lower():
                    url = self.base_link+url
                    print url
                    self.get_source(url,title,year,'','',start_time)
            return self.sources
        except:
            pass
            return[]

    def get_source(self,link, title, year, season, episode, start_time):
        try:
            headers={'User-Agent':User_Agent}
            html = requests.get(link,headers=headers,timeout=5).content
            match = re.compile('var link_server.+?"(.+?)"',re.DOTALL).findall(html)
            count = 0
            for link in match:
                if not link.startswith('https:'):
                    link = 'http:' + link
                if 'vidnode' in link:
                    if not 'load.php' in link:
                        continue
                    #print 'vidnodelink >>> '+link
                    html = requests.get(link).content
                    
                    grab = re.compile("sources.+?file: '(.+?)',label: '(.+?)'",re.DOTALL).findall(html)
                    for end_link,rez in grab:
                        if '1080' in rez:
                            res = '1080p'
                        elif '720' in rez:
                            res= '720p'
                        else: res = 'SD'
                        count +=1
                        self.sources.append({'source': 'Vidnode', 'quality': res, 'scraper': self.name, 'url': end_link, 'direct': False})
                
                elif urlresolver.HostedMediaFile(link).valid_url():
                    host = link.split('//')[1].replace('www.','')
                    host = host.split('/')[0].split('.')[0].title()
                    count +=1
                    self.sources.append({'source': host, 'quality': 'SD', 'scraper': self.name, 'url': link, 'direct': False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year, season=season,episode=episode)

        except:
            pass



import re,xbmcaddon,time 
import resolveurl,requests
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

class mvlinks(Scraper):
    domains = ['http://dl.newmyvideolink.xyz']
    name = "MyVideoLinks"
    sources = []

    def __init__(self):
        self.base_link = 'http://go.myvideolinks.net'
        self.uniques = []
        self.sources = []
        self.count = 0

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_time = time.time()
            search_id = clean_search(title.lower())
            season_pull = "0%s"%season if len(season)<2 else season
            episode_pull = "0%s"%episode if len(episode)<2 else episode
                   
            movie_url = '%s/?s=%s+S%sE%s' %(self.base_link,search_id.replace(' ','+'),season_pull,episode_pull)
            #print ' ##search## %s | %s' %(self.name,movie_url)
            headers = {'User_Agent':User_Agent}
            link = requests.get(movie_url,headers=headers,timeout=10).content
            
            links = link.split('post-title')
            for p in links:

                m_url = re.compile('href="([^"]+)"').findall(p)[0]
                m_title = re.compile('title="([^"]+)"').findall(p)[0]
                #print 'gw>> URL>  '+m_url
                #print 'gw>> TITLE> '+m_title
                if not 's%se%s' %(season_pull,episode_pull) in m_title.lower():
                    continue
                if not clean_title(title).lower() in clean_title(m_title).lower():
                    continue
                #print ' ##Item to pass## %s | %s' %(self.name,m_url)
                self.get_source(m_url,title,year,season,episode,start_time)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources
        
    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            links_send = 0
            search_id = clean_search(title.lower())
            movie_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            print ' ##search## %s | %s' %(self.name,movie_url)
            headers = {'User_Agent':User_Agent}
            
            link = requests.get(movie_url,headers=headers,timeout=5).content
            
            links = link.split('post-title')
            for p in links:

                m_url = re.compile('href="([^"]+)"').findall(p)[0]
                m_title = re.compile('title="([^"]+)"').findall(p)[0]
                #print 'gw>> URL>  '+m_url
                #print 'gw>> TITLE> '+m_title
                if ' 20' in m_title:
                    name = m_title.split(' 20')[0]
                elif ' 19' in m_title:
                    name = m_title.split(' 19')[0]
                else:
                    name = m_title
                    
                if not clean_title(title).lower() == clean_title(name).lower():
                    continue
                if not year in m_title.lower():
                    continue
                links_send +=1
                if links_send <4:
                    print ' ##Item to pass## %s | %s' %(self.name,m_url)
                    self.get_source(m_url,title,year,'','',start_time)
                else:pass
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

    def get_source(self,m_url,title,year,season,episode,start_time):

        try:
            #print ' ##get_sources## %s | %s' %(self.name,m_url)
            
            OPEN = requests.get(m_url).content
            match = re.compile('<li><a href="(.+?)"').findall(OPEN)
            
            for link in match:
                if not resolveurl.HostedMediaFile(link).valid_url(): 
                    continue                
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                
                if link not in self.uniques:
                    self.uniques.append(link)
                    if '1080' in link:
                        rez='720p'
                    elif '720' in link:
                        rez='720p'
                    else: 
                        rez='DVD'
                    self.count +=1
                    self.sources.append({'source': host,'quality': rez,'scraper': self.name,'url': link,'direct': False})
        except:pass
        try:
            alt_url = m_url+'2/'
            
            alt = requests.get(alt_url).content
            match = re.compile('<li><a href="(.+?)"').findall(alt)
            for link in match:
                if not resolveurl.HostedMediaFile(link).valid_url(): 
                    continue                
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                if link not in self.uniques:
                    if '1080' in link:
                        rez='720p'
                    elif '720' in link:
                        rez='720p'
                    else: 
                        rez='DVD'
                    self.uniques.append(link)
                    self.count +=1
                    self.sources.append({'source': host,'quality': rez,'scraper': self.name,'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,self.count,title,year, season=season,episode=episode)

        except:
            pass

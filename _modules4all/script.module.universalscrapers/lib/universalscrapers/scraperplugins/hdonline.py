import requests
import re,time
import xbmc
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log 
dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")
  
class hdonline(Scraper):
    domains = ['https://hdonline.is']
    name = "hdonline"
    sources = []

    def __init__(self):
        self.base_link = 'https://hdonline.is'
        if dev_log=='true':
            self.start_time = time.time() 


    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())                                     # use 'clean_search' to get clean title 
            start_url = '%s/search/%s' %(self.base_link,search_id.replace(' ','+'))         # construct search url attributes using site url
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content 
            match = re.compile('class="movie-item".+?<a href="(.+?)" title="(.+?)"',re.DOTALL).findall(html) # Regex info on results page
            for item_url, name in match:
               # print 'item_url>>>>>>>>>>>>>> '+item_url                                # use print statments to confirm grabs check log
               # print 'name>>>>>>>>>>>>>> '+name
                if clean_title(search_id).lower() == clean_title(name).lower():     # confirm name use 'clean_title' this will remove all unwanted
                                                                                        # incuding spaces to get both in same format to match if correct
                        print 'Send this URL> ' + item_url
                        OPEN = requests.get(item_url,headers=headers,timeout=5).content
                        rel = re.findall('<div class="dcis dcis-03">Released:(.+?)</div>',OPEN)[0]
                        qual = re.findall('<div class="dcis dcis-02">Quality: <span class="badge">(.+?)</span></div>',OPEN)[0]
                        #print qual  
                        if year == rel.strip():
                            end = re.compile('data-movie="(.+?)"').findall(OPEN)[0]
                            a1 = 'https://hdonline.is/ajax/movie/episodes/'+end 
                            #print a1
                            Open_a1 = requests.get(a1,headers=headers).content
                           # print Open_a1
                            ID = re.compile('data-id=(.+?)id=',re.DOTALL).findall(Open_a1)
                            for ep in ID:
                                #print ep
                                if 'class' in ep: 
                                    pass
                                else: 
                                    ep =  ep.replace('\\"','').strip()
                                    url = 'https://hdonline.is/ajax/movie/token?eid='+ep+'&mid='+end
                                    #print url                              # confirm in log correct url(s) sent to get_source
                                    self.get_source(url,ep,qual)                                       # send url to next stage
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            SS = "0%s"%season if len(season)<2 else season
            EE = "0%s"%episode if len(episode)<2 else episode
            search_term = clean_search(title.lower())+' '+'season'+SS
            search_id = clean_search(title.lower())
            search = '%s/search/%s'  %(self.base_link,search_term.replace(' ','+'))
            headers={'User-Agent':random_agent()}
            html = requests.get(search,headers=headers,timeout=20).content 
            match = re.compile('class="movie-item".+?<a href="(.+?)" title="(.+?)"',re.DOTALL).findall(html) # Regex info on results page
            for item_url, name in match:
                seas = re.sub('[^0-9]','',name)
                title = re.sub('[^a-z ]','',name.lower().replace('season',''))
                #print title
                seas = "0%s"%seas if len(seas)<2 else seas
                #print name
                if clean_title(search_id).lower() in clean_title(name).lower():
                    if seas == SS:
                        #print '>>>>>>>>>>'+item_url
                        OPEN = requests.get(item_url,headers=headers,timeout=20).content
                        rel = re.findall('<div class="dcis dcis-03">Released:(.+?)</div>',OPEN)[0]
                        qual = re.findall('<div class="dcis dcis-02">Quality: <span class="badge">(.+?)</span></div>',OPEN)[0]
                        #print qual  
                        if show_year == rel.strip():
                            end = re.compile('data-movie="(.+?)"').findall(OPEN)[0]
                            a1 = 'https://hdonline.is/ajax/movie/episodes/'+end 
                            #print a1
                            Open_a1 = requests.get(a1,headers=headers).content
                           # print Open_a1
                            block = re.compile('data-id="(.+?)".+?title=".+?>(.+?)<').findall(Open_a1.replace('\\',''))
                            for ID,info in block:
                                if 'Episode' in info:
                                    eps = re.findall('Episode (.+?):',str(info))[0]
                                    if len(episode) == 1:
                                        episode = '0'+episode
                                    if episode == eps:
                                        url = 'https://hdonline.is/ajax/movie/token?eid='+ID+'&mid='+end
                                        self.get_source(url,ID,qual)                                       
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')  

    def get_source(self,url,ep,qual):
        try:
            headers={'User-Agent':random_agent()}
            html3 = requests.get(url,headers=headers,timeout=5).content
            #print html3
            count = 0
            x,y = re.findall("_x='(.+?)', _y='(.+?)'",html3)[0]
            #print x
            url2 = 'https://hdonline.is/ajax/movie/get_sources/'+ep+'?x='+x+'&y='+y
            #print url2
            h = requests.get(url2,headers=headers,timeout=5).content
            #print h
            if '"file"' in h:
                playlink = re.findall('"file":"(.+?)"',h)[0]
                link = playlink.replace('\\','')
                count +=1
                #print link
                host = link.split('//')[1].replace('www.','')
                #print host
                hostname = host.split('.com')[0].title()
                #print hostname
                self.sources.append({'source': hostname, 'quality': qual, 'scraper': self.name, 'url': link,'direct': False})
            elif '"src"' in h:
                playlink = re.findall('"src":"(.+?)"',h)[0]
                link = playlink.replace('\\','')
                count +=1
                #print link
                host = link.split('//')[1].replace('www.','')
                hostname = host.split('/')[0].title()
                self.sources.append({'source': hostname, 'quality': qual, 'scraper': self.name, 'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,count)
          
        except:
            pass
#hdonline().scrape_episode('kingpin', '2018', '', '1', '2', '', '')
#hdonline().scrape_movie('black water', '2018','')
# you will need to regex/split or rename to get host name if required from link unless available on page it self 

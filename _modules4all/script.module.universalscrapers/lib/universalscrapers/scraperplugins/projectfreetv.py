import re
import requests,time
import xbmc,xbmcaddon
from ..scraper import Scraper
from ..common import clean_title,clean_search,filter_host,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class projectfreetv(Scraper):

    domains = ['http://projectfreetv.bz/']
    name = "ProjectFree"
    sources = []

    def __init__(self):
        self.base_link = 'http://projectfreetv.bz/'
        
                          
    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_time = time.time()
            headers = {'User-Agent':random_agent()}
            search_id = clean_search(title.lower())
            start_url= '%s?s=%s' %(self.base_link,search_id.replace(' ','%20'))
            html = requests.get(start_url,headers=headers,timeout=5).content
            #print html
            #print start_url
            match = re.compile('<td>.+?<a href="(.+?)"><b>(.+?)</b></a>',re.DOTALL).findall(html)
            for url,name in match:
                #print url,name
                if search_id == name.lower():
                    #print url,name
                    sehtml = requests.get(url,headers=headers,timeout=5).content
                    seas1 = re.compile('class="mnlcategorylist".+?href="(.+?)"><b>Season (.+?)</b>',re.DOTALL).findall(sehtml)
                    for seaurl,seas in seas1:
                        #print seaurl,seas
                        if seas == season:
                            #print seaurl,seas
                            html2 = requests.get(seaurl,timeout=5).content
                            #print html2
                            match2 = re.compile('<a href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html2)
                            for url2, name2 in match2:
                                #print name2
                                #print'url2><><><><><><><><><><'+url2
                                episodes = re.findall('Episode (.+?)>',str(name2)+'>')
                                for episod in episodes:
                                    #print episod
                                    if episode == episod:
                                        self.get_source(url2,title,year,season,episode,start_time)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources                           

    # def scrape_movie(title, year, debrid = False):
    #     try:
    #         start_url= search_movie+title.replace(' ','%20')
    #         html = requests.get(start_url,timeout=3).content
    #         match = re.compile('<div style="float:left.+?href="(.+?)" title="(.+?)"',re.DOTALL).findall(html)
    #         for url,name in match:
    #             movie_year = re.findall('\((.+?)\)',str(name))[0]
    #             url = base_link+url
    #             if movie_year == year:
    #                 name = re.findall('(.+?) \(',str(name))[0]
    #                 if title.lower() in name.lower():
    #                     get_source(url)
    #         return sources
    #     except Exception as e:
    #         print scraper_name + ' : '+ str(e)
    #         return []     

    def get_source(self,url2, title, year, season, episode, start_time):
        try:
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(url2,headers=headers,timeout=5).content
            count = 0
            Endlinks = re.compile('href="/external(.+?)"',re.DOTALL).findall(OPEN)
            for link1 in Endlinks:
                count +=1
                link=link1.replace('.php?url=','')
                #print link +'<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
                if '1080' in link:
                    qual='1080p'
                elif '720' in link:
                    qual='720p'
                else:
                    qual='SD'
            
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0]
                if not filter_host(host):
                        continue
                host = host.split('.')[0].title()
                self.sources.append({'source': host,'quality': qual,'scraper': self.name,'url': link,'direct': False})

            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year, season=season,episode=episode)
            return []
        except:
            pass

#projectfreetv().scrape_episode('the blacklist', '2013', '2017', '5', '6', '', '')

import re
import requests,time
import xbmc,xbmcaddon
from BeautifulSoup import BeautifulSoup as bs
from ..scraper import Scraper
from ..common import clean_search, random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")
session = requests.session()

class projectfreetvmovies(Scraper):
    domains = ['projectfreetvmovies.info']
    name = "PFTM"
    sources = []
    def __init__(self):
        self.base_link = 'http://projectfreetvmovies.info'
        self.search = self.base_link+'/?s='
        if dev_log=='true':
            self.start_time = time.time()
                              
    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url = self.search+title.replace(' ','+')
            #print start_url
            html = requests.get(start_url,timeout=5).content
            match = re.compile('class="ml-item"><a href="(.+?)".+?alt="(.+?)">').findall(html)
            for url,name in match:
                if clean_search(title).replace(' ','')==clean_search(name).replace(' ',''):
                    html2 = bs(requests.get(url).content)
                    #print html2
                    season_blocks = html2.findAll('div',attrs={'class':'tvseason'})
                    for season_block in season_blocks:
                        season_check = re.findall('<strong>Season (.+?)</strong>',str(season_block))[0]
                        if season_check == season:
                            episodes = re.findall('<a href="(.+?)">Episode (.+?) </a>',str(season_block))
                            for fin_url,episode_ in episodes:
                                if episode == episode_:
                                    print fin_url
                                    self.get_source(fin_url)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return []                           

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_url= self.search+title.replace(' ','+')
            print start_url
            html = requests.get(start_url,timeout=5).content
            #print html
            match = re.compile('class="ml-item"><a href="(.+?)".+?alt="(.+?)">').findall(html)
            for url,name in match:
                #print url,name
                if clean_search(title).replace(' ','')==clean_search(name).replace(' ',''):
                    print url,name
                    self.get_source(url)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return []                           

    def get_source(self,url):
        try:
            get_cookies = session.get(url).content
            cookie_frame = re.findall('<iframe src="(.+?)"',get_cookies)
            count = 0
            for cookie_page in cookie_frame:
                if 'putstream' in cookie_page:
                    html2 = session.get(cookie_page,allow_redirects=True).content
                    #print html2
                    get_cookie_info = re.compile("var tc = '(.+?)'.+?url: \"(.+?)\".+?\"_token\": \"(.+?)\".+?function _tsd_tsd_ds\(s\)(.+?)</script>",re.DOTALL).findall(html2)
                    for tokencode, url_to_open,_token,xtokenscript in get_cookie_info:
                        #print tokencode,xtokenscript, url_to_open,_token
                        x_token = get_x_token(tokencode,xtokenscript)
                        #print x_token
                        headers = {'User-Agent':random_agent(),
                                   'Host':'gomostream.com',
                                   'Referer':cookie_page,
                                   'x-token':x_token}
                        data = {'tokenCode':tokencode,
                                '_token':_token}
                        html3 = session.post(url_to_open,headers=headers,data=data).json()
                        for playlink in html3:
                            count +=1
                            if playlink!='':
                                try:
                                    if playlink[0]==' ':
                                        playlink = playlink[1:]
                                except:
                                    playlink = playlink
                                try:
                                    source = re.findall('//(.+?)/',str(playlink))[0]
                                except:
                                    source = self.name
                                self.sources.append({'source': source, 'quality': 'HD', 'scraper': self.name, 'url': playlink,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count) 
        except:
            pass 
            return []

def get_x_token(tokencode,xtokenscript):
    #print tokencode,xtokenscript
    start,finish,add1,add2 = re.findall('slice\((.+?),(.+?)\).+?\+ "(.+?)"\+"(.+?)"',str(xtokenscript))[0]
    #print start,finish,add1,add2
    split = tokencode[int(start):int(finish)]
    reverse = split[::-1]
    x_token = str(reverse)+add1+add2
    return x_token

#scrape_episode('the blacklist', '2013', '2017', '5', '3')
#scrape_movie('bright', '2016')

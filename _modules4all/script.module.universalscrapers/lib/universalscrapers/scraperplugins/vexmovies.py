import requests
import re
####### kodi #########
import xbmc
import xbmcaddon
import time
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title,clean_search,random_agent,send_log,error_log
####### idle #########
# dev_log = 'true'
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")
session = requests.Session()

user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
class vexmovies(Scraper):
    domains = ['http://vexmovies.org']
    name = "VexMovies"
    sources = []

    def __init__(self):
        self.base_link = 'http://vexmovies.org'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            headers={'User-Agent':user_agent}
            html = session.get(start_url,headers=headers,timeout=5).content
            match = re.compile('id="mt-.+?href="(.+?)">.+?alt="(.+?)".+?<span class="year">(.+?)</span>.+?class="calidad2">(.+?)</span>',re.DOTALL).findall(html)
            for item_url,name,release,qual in match:
                if year == release:
                    if clean_title(search_id).lower() == clean_title(name).lower():                              
                        self.get_source(item_url,qual,title,year,start_time)                                      
            return self.sources
        except Exception, argument:
            #print argument
            if dev_log == 'true':
                error_log(self.name,argument)

    def get_source(self,item_url,qual,title,year,start_time):
        try:
            #print item_url
            #print 'hi'
            count = 0
            headers={'User-Agent':random_agent()}
            OPEN = session.get(item_url,headers=headers,timeout=5).content           
            Endlinks = re.compile('class="entry-content">.+?<iframe src="(.+?)".+?</iframe>',re.DOTALL).findall(OPEN)
            for link in Endlinks:
                headers={'User-Agent':user_agent, 'Host':'consistent.stream',
                         'Referer':item_url}
                #print link
                consistant = session.get(link,headers=headers,timeout=5).content
                video_, Hash = re.findall('video="(.+?)" hash="(.+?)"',consistant)[0]
                api_url = 'https://consistent.stream/api/getVideo'
                headers={'User-Agent':user_agent, 'Host':'consistent.stream','Referer': 'https://consistent.stream/titles/'+video_}
                #print video_
                #print Hash
                data = {'key':Hash,'referrer':item_url,'video':video_}
                api_html = session.post(api_url,headers=headers,data=data).content
                #print str(api_html)
                #### trying to get response from api_url but being a nob
               #consistant = self.replace_html_entities(consistant)
                final_links = re.compile('"src":"(.+?)"',re.DOTALL).findall(api_html)
                #print str(final_links)
                for links in final_links:
                
                    irl= 'irl-'
                    gool = 'googleusercontent'
                    if irl not in links:
                        if gool not in links:
                            links = links.replace('\\','')
                            host = links.split('//')[1].replace('www.','')
                            hostname = host.split('/')[0].split('.')[0].title()
                            if 'mentor' in links:
                                links = links +'|'+'User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0&Referer='+link
                                count += 1
                                self.sources.append({'source': hostname, 'quality': qual, 'scraper': self.name, 'url': links,'direct': False})
                            else:
                                count += 1
                                self.sources.append({'source': hostname, 'quality': qual, 'scraper': self.name, 'url': links,'direct': False})   
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            #print argument
            if dev_log == 'true':
                error_log(self.name,argument)

    def replace_html_entities(self,string):
        List = [['&lt;','<'],['&#60;','<'],['&gt;','>'],['&#62;','>'],['&amp;','&'],['&#38;','&'],
                ['&quot;','"'],['&#34;','"'],["&apos;","'"],["&#39;","'"],['\\/','/']]
        for item in List:
            string = string.replace(item[0],item[1])
        return string

#vexmovies().scrape_movie('Deadpool', '2016','')

import requests
import re
import xbmc
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent

  
class bmovies(Scraper):
    domains = ['https://bmoviesfree.net']
    name = "bmovies"
    sources = []

    def __init__(self):
        self.base_link = 'https://bmoviesfree.net'
        self.Session = requests.Session()



    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())                                     # use 'clean_search' to get clean title 
                                                                                        #(movie name keeping spaces removing excess characters)

            search_url = '%s/search-query/%s/' %(self.base_link,search_id.replace(' ','+'))         # construct search url attributes using site url
            #print '::::::::::::: START URL '+search_url                                  # print to log to confirm 
            search_response = self.Session.get(search_url).content
            search_regex = re.findall('<a class="poster".+?href="(.+?)".+?onclick=.+?onclick=.+?>(.+?)<',search_response,re.DOTALL)
            for search_result_url, search_result_name in search_regex:
                #print 'item_url>>>>>>>>>>>>>> '+search_result_url                                # use print statments to confirm grabs check log
                #print 'name>>>>>>>>>>>>>> '+search_result_name
                #if year in name:                                                        # confirm year if available in results sometines in name grab/or regex elsewhere
                    
                if clean_title(search_id).lower() == clean_title(search_result_name).lower():     # confirm name use 'clean_title' this will remove all unwanted
                                                                                        # incuding spaces to get both in same format to match if correct
                        #print 'Send this URL> ' + search_result_url                              # confirm in log correct url(s) sent to get_source
                        self.get_source(search_result_url,search_url,year)                                       # send url to next stage
            return self.sources
        except:
            pass
            return[]

            
    def get_source(self,search_result_url,search_url,year):
        try:
            get_start_url_html = self.Session.get(search_result_url).content
            #print get_start_url_html
            get_start_url_regex = re.findall('<div id="player">.+?href="(.+?)".+?alt="(.+?)"',get_start_url_html,re.DOTALL)
            for start_url,alt in get_start_url_regex:
                if year in alt:
                    #print start_url
                    start_url = start_url.replace('//','/').replace('https:/','https://')
                    #print start_url
                    start_headers = {'Host':'bmoviesfree.net','Referer':search_url}
                    start_html = self.Session.get(start_url, headers = start_headers).content
                    start_regex = re.findall('data-streamgo="(.+?)"',start_html)
                    headers = {'Referer':start_url, 'Host':'streamgo.me'}
                    for start_link in start_regex:
                        url = 'https://streamgo.me/player/'+start_link
                        #print url
                        host = url.split('//')[1].replace('www.','')
                        host = host.split('/')[0].split('.')[0].title()
                        html = self.Session.get(url, headers=headers).content
                        regex = re.findall('sources: \[\{"file":"(.+?)"',html)
                        for link in regex:
                            headers = {'Referer':url, 'Host':'streamgo.me'}
                            playlink_html = self.Session.get(link, headers=headers).content
                            file_end = re.findall('(.+?)\n',playlink_html+'\n')
                            for single_line in file_end:
                                if 'm3u8' in single_line:
                                    playlink = link.replace('video.m3u8',single_line)+'|Host=mango.fruity.pw&Origin=http://stramgo.me'
                                    self.sources.append({'source': host , 'quality': 'SD', 'scraper': self.name, 'url': playlink,'direct': False}) #this line will depend what sent     
        except:
            pass
#bmovies().scrape_movie('tomb raider','2018','')
# you will need to regex/split or rename to get host name if required from link unless available on page it self 

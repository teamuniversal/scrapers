import requests, re
import resolveurl as urlresolver
import urlparse
import xbmcaddon, time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class movienolimit(Scraper):
	domains = ['http://movienolimit.to']
	name = "MovienoLimit"
	sources = []

	def __init__(self):
		self.base_link = 'http://movienolimit.to'
		if dev_log=='true':
			self.start_time = time.time()

	def scrape_movie(self,title,year,imdb, debrid = False):
		try:
		    search_id = clean_search(title.lower())	
		    start_url = '%s/search?query=%s' %(self.base_link,search_id.replace(' ','+'))
#		    print '>>>>>start_url>>>>>>>>' +start_url
		    headers = {'User_Agent':random_agent()}
		    html = requests.get(start_url,headers=headers,timeout=5).content
		    match = re.compile('class="movie-title".+?href="(.+?)">(.+?)</a>',re.DOTALL).findall(html)
		    for item_url,name in match:
		    		if clean_title(title)==clean_title(name):
		    			item_url1 = self.base_link+item_url
		    			#print '>>>>item_url1>>>>>>>>>>' +item_url1 
		    			#print '>>>>name>>>>>>>>>>>>>>>' +name
		    			self.get_source(item_url1,year)
		    return self.sources
		except Exception, argument:
			if dev_log == 'true':
				error_log(self.name,'Check Search') 
			return self.sources
			
	def get_source(self,item_url1,year):
		try:
			#print '>>>>>movienolimit_PASS>>>>>>>>>>>' +item_url1
			headers={'User_Agent':random_agent()}
			OPEN = requests.get(item_url1,headers=headers,timeout=5).content
			#print OPEN
			year_chk = re.compile('<div>Release Year:.+?">(.+?)<',re.DOTALL).findall(OPEN)
			if year in year_chk:
				print '>>>>year>>>>>>' +year
				Endlinks = re.compile(">Play:.+?onclick=.+?'(.+?)'",re.DOTALL).findall(OPEN)
				count = 0 
				for link in Endlinks:
					link = self.base_link + link
					headers = {'User-Agent': random_agent()}
					r = requests.get(link,headers=headers,allow_redirects=False)
					link = r.headers['location'] 
					#print '>>>>>>>>>>play_link>>>>>>>>>'     +link
					if urlresolver.HostedMediaFile(link):
							host = link.split('//')[1].replace('www.','')
							host = host.split('/')[0].split('.')[0].title()
							count +=1
							self.sources.append({'source':host,'quality':'DVD','scraper':self.name,'url':link,'direct':False})

				if dev_log=='true':
					end_time = time.time() - self.start_time
					send_log(self.name,end_time,count)
		except:
			pass



							
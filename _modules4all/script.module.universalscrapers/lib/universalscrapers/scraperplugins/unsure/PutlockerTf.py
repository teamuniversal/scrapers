
### has to open too many pages
import requests
import re
import base64
import time
########## kodi imports ###########
import xbmc
import xbmcaddon
import time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log 
# from ..modules import cfscrape
############# idle imports for testing ##########
# from nanscrapers.common import clean_title,clean_search,random_agent
# from nanscrapers.modules import cfscrape
#dev_log = 'true'
############### idle ##########

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class putlockertf(Scraper):
	domains = ['http://www1.putlockers.tf']
	name = "PutlockerTf"
	sources = []

	def __init__(self):
		self.base_link = 'http://www1.putlockers.tf'
	  


	def scrape_movie(self, title, year, imdb, debrid = False):
		try:
			start_time = time.time()
			search_id = clean_search(title.lower())
			start_url = '%s/search-movies/%s.html' %(self.base_link,search_id.replace(' ','+'))
			print '::::::::::::: START URL '+start_url
			headers={'User-Agent':random_agent()}
			html = requests.get(start_url,headers=headers,timeout=5).content
			match = re.compile('class="ml-item".+?href="(.+?)".+?<i>(.+?)</i>.+?Release:(.+?)</b>',re.DOTALL).findall(html)
			for item_url,name,release in match:
				#yrz=release.strip()
				if year in release:
					if clean_title(search_id).lower() == clean_title(name).lower():                                    
						print 'Send this URL> ' + item_url                              
						self.get_source(item_url,title,year,'','',start_time)
			return self.sources
		except:
			pass
			return[]
  
	def get_source(self,item_url, title, year, season, episode, start_time):
		try:
			start_time = time.time()
			headers={'User-Agent':random_agent()}
			OPEN = requests.get(item_url,headers=headers,timeout=5).content
			block = re.compile('id="cont_player">(.+?)alt="You May Also Like',re.DOTALL).findall(OPEN)
			servs = re.compile('class="server_line".+?href="(.+?)".+?class="server_servername".+?</a>.+?</div>',re.DOTALL).findall(str(block))
			for servers in servs:
				get_server = requests.get(servers,headers=headers,timeout=5).content
				Endlinks = re.compile('id="media-player".+?Base64.decode.+?"(.+?)".+?</div>',re.DOTALL).findall(get_server)
				for encoded in Endlinks:
					decoded = base64.b64decode(encoded)
					final_link = re.compile('<iframe.+?src="(.+?)".+?</iframe>',re.DOTALL).findall(str(decoded))
					count = 0
					for link in final_link:
						# xbmc.log('************ LOG THIS '+repr(link),xbmc.LOGNOTICE)
						label = 'SD'
						host = link.split('//')[1].replace('www.','')
						hostname = host.split('/')[0].split('.')[0].title()
						count +=1
						# xbmc.log('************ LOG THIS '+repr(count),xbmc.LOGNOTICE)
						self.sources.append({'source': hostname, 'quality': label, 'scraper': self.name, 'url': link,'direct': False})   
			if dev_log=='true':
				end_time = time.time() - start_time
				send_log(self.name,end_time,count,title,year, season=season,episode=episode)
		
		except:
			pass

# putlockertf().scrape_movie('Justice League', '2017','')

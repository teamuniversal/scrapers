import universalscrapers
import xbmcgui
import os,re
import xbmc
import xbmcaddon
import random
import sys
import urlparse
import xbmcvfs
import time
import urllib
import xbmc
import xbmcgui
import xbmcplugin
from universalscrapers.common import clean_title
from BeautifulSoup import BeautifulStoneSoup
dialog = xbmcgui.Dialog()
pDialog = xbmcgui.DialogProgress()
No_of_scrapers = []
scraper_paths = []

ADDON_PATH = xbmc.translatePath('special://home/addons/script.module.universalscrapers/')
ICON = ADDON_PATH + 'icon.png'
FANART = ADDON_PATH + 'fanart.jpg'

scraper_results_path = xbmc.translatePath('special://home/userdata/addon_data/script.module.universalscrapers/Log.txt')
if not os.path.exists(scraper_results_path):
	Open = open(scraper_results_path,'w+')
	
scrapers_path = xbmc.translatePath('special://home/addons/script.module.universalscrapers/lib/universalscrapers/scraperplugins')
for Root, Dir, Files in os.walk(scrapers_path):
	for File in Files:
		if not 'pyo' in File and not '__' in File and 'py' in File and not 'broken' in Root and not 'slow' in Root and not 'ok' in Root and not 'unsure' in Root and not 'test' in Root:
			No_of_scrapers.append('1')
			scraper_paths.append(File)

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))
mode = params.get('mode')
if mode == "DisableAll":
    scrapers = sorted(
        universalscrapers.relevant_scrapers(include_disabled=True), key=lambda x: x.name.lower())
    for scraper in scrapers:
        key = "%s_enabled" % scraper.name
        xbmcaddon.Addon('script.module.universalscrapers').setSetting(key, "false")
    sys.exit()
elif mode == "EnableAll":
    scrapers = sorted(
        universalscrapers.relevant_scrapers(include_disabled=True), key=lambda x: x.name.lower())
    for scraper in scrapers:
        key = "%s_enabled" % scraper.name
        xbmcaddon.Addon('script.module.universalscrapers').setSetting(key, "true")
    sys.exit()
elif mode == "Deletelog":
    from universalscrapers.common import Del_LOG
    Del_LOG()
    sys.exit()

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

movies = [
    {
        'title': 'Deadpool',
        'year': '2016',
        'imdb': 'tt1431045'
    },
    {
        'title': 'Silence',
        'year': '2016',
        'imdb': 'tt0490215'
    },
    {
        'title': 'Logan',
        'year': '2017',
        'imdb': ''
    },
    {
        'title': 'The Great Wall',
        'year': '2016',
        'imdb': 'tt2034800'
    },
    {
        'title': 'Why Him?',
        'year': '2016',
        'imdb': 'tt4501244'
    },
    {
        'title': 'Patriots Day',
        'year': '2016',
        'imdb': 'tt4572514'
    },
    {
        'title': 'Baywatch',
        'year': '2017',
        'imdb': ''
    },
    {
        'title': 'Sing',
        'year': '2016',
        'imdb': 'tt3470600'
    },
    {
        'title': 'Sonic The Hedgehog: The Movie',
        'year': '1996',
        'imdb': 'tt0237765'
    },
    {
        'title': 'Surf\'s Up',
        'year': '2007',
        'imdb': 'tt0423294'
    },
    {
        'title': 'Kim Possible A Sitch in Time',
        'year': '2004',
        'imdb': 'tt0389074'
    },
    {
        'title': 'Izzies Way Home',
        'year': '2016',
        'imdb': 'tt5667482'
    },
    {
        'title': 'A Turtle\'s Tale: Sammy\'s Adventures',
        'year': '2010',
        'imdb': 'tt1230204'
    },
]

shows = [
    {
        'title': "The Flash",
        'show_year': "2014",
        'year': "2014",
        'season': '1',
        'episode': '1',
        'imdb': 'tt3107288',
    },
    {
        'title': "The Flash",
        'show_year': "2014",
        'year': "2016",
        'season': '3',
        'episode': '8',
        'imdb': 'tt3107288',
    },
    {
        'title': "Breaking Bad",
        'show_year': "2008",
        'year': "2008",
        'season': '1',
        'episode': '1',
        'imdb': 'tt0903747',
    },
    {
        'title': "Breaking Bad",
        'show_year': "2008",
        'year': "2011",
        'season': '4',
        'episode': '6',
        'imdb': 'tt0903747',
    },
    {
        'title': "Game of Thrones",
        'show_year': "2011",
        'year': "2011",
        'season': '1',
        'episode': '1',
        'imdb': 'tt0944947',
    },
    {
        'title': "Game of Thrones",
        'show_year': "2011",
        'year': "2016",
        'season': '6',
        'episode': '5',
        'imdb': 'tt0944947',
    },
    {
        'title': "House M.D.",
        'show_year': "2004",
        'year': "2004",
        'season': '1',
        'episode': '1',
        'imdb': 'tt0412142',
    },

]

num_shows = len(shows) + len(movies)

def main():
    test_type = xbmcgui.Dialog().select("Choose type of test", ["Test Scrapers" , "Check Scraper Results" , "Wipe Scraper Results"])
    basepath = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile"))
    if test_type == 0:
        test()
    elif test_type == 1:
        if os.path.exists(scraper_results_path):
            get_scraper_results()
        else:
            xbmcgui.Dialog().notification("Oopsie Daisy", "File not found")
    elif test_type == 2:
		clear_scraper_log()
	
def clear_scraper_log():
	if os.path.exists(scraper_results_path):
		Open = open(scraper_results_path,'w+')
	else:
		xbmcgui.Dialog().notification("Oopsie Doodles", "File not found")

def get_scraper_results():
	try:
		results_type = xbmcgui.Dialog().select("Choose type of results", ["Full" , "Slow Scrapers" , "No Results", "Errors"])
		slow_scraper_list = []
		no_results = []
		scraper_names = []
		scraper_results_check_name = []
		for item in scraper_paths:
			Scraper_path = os.path.join(scrapers_path,item)
			get_scraper_names = re.findall('name = "(.+?)"',open(Scraper_path).read())
			for name in get_scraper_names:
				scraper_names.append(name)
		if not os.path.exists(scraper_results_path):
			Open = open(scraper_results_path,'w+')
		else:
			Open = open(scraper_results_path).read()
			get_info = re.findall('<.+?universalscraper: (.+?)\n.+?Tested with: (.+?)\n.+?Links returned: (.+?)\n.+?Time to Complete:(.+?)\n',str(Open),re.DOTALL)
			for scraper_name, info_tested, no_of_links, time_taken in get_info:
				scraper_results_check_name.append(scraper_name)
				dict_string = {'scraper_name':scraper_name, 'info_tested':info_tested,'no_of_links':no_of_links,'time_taken':time_taken}
				if round(float(time_taken)) > 10:
					slow_scraper_list.append(dict_string)				
		for name in scraper_names:
			if name not in str(scraper_results_check_name):
				no_results.append(name)
		if results_type == 0:
			Open = open(scraper_results_path).read()
			get_line = re.findall('(.+?)\n',Open,re.DOTALL)
			dialog.textviewer("universalscrapers Testing Mode", '\n'.join(str(p) for p in get_line) )
		elif results_type == 1:
			if len(slow_scraper_list)==0:
				dialog.textviewer("Scrapers with slow times",'No Scrapers took over 10 seconds')
			else:
				dialog.textviewer("Scrapers with slow times", '\n'.join(str(scraper['scraper_name']+' : returned '+str(scraper['no_of_links']).replace('Check Scraper/NoLinks','0')+' links for '+scraper['info_tested']+' in '+scraper['time_taken']+' seconds') for scraper in slow_scraper_list) )
				
		elif results_type == 2:
			dialog.textviewer("Scrapers with no results", '\n'.join(str(p) for p in no_results) )
		elif results_type == 3:
			List = []
			Open = open(scraper_results_path).read()
			get_errors = re.findall(':>>>>(.+?)\n:>>>>(.+?)\n',Open,re.DOTALL)
			for line1, line2 in get_errors:
				List.append(line1.replace('  ',''))
				List.append(line2.replace('  ',''))
				List.append('\n')
				List.append('#######################')
			dialog.textviewer("Scraper Errors", '\n'.join(str(p) for p in List) )
	except Exception as e:
		xbmcgui.Dialog().notification("Oopsie Daisy", str(e))
			
def disable_working(scraper_id):
    key = "%s_enabled" % scraper_id
    xbmcaddon.Addon('script.module.universalscrapers').setSetting(key, "false")
    sys.exit()
			
def test():
	pDialog = xbmcgui.DialogProgress()
	if dialog.yesno("universalscrapers Testing Mode", 'Clear Scraper Log?'):
		clear_scraper_log()
	if dialog.yesno("universalscrapers Testing Mode", 'Clear cache?'):
		universalscrapers.clear_cache()
	test_type = xbmcgui.Dialog().select("Choose type of test", ["Single Scraper" , "Full Test" ])
	if test_type == 0:
		single_test(0,0)
	elif test_type == 1:
		full_test()
		
def single_test(count, index):
	if count==5:
		pass
	else:
		Scrapers_Run = 0
		Movies = movies[count]
		tv_shows = shows[count]
		pDialog.create('universalscrapers Testing mode active', 'please wait')
		if dialog.yesno("universalscrapers Testing Mode", 'Run next Movie?',Movies['title']+' ('+Movies['year']+')'):
			movie_links_scraper = universalscrapers.scrape_movie(Movies['title'], Movies['year'], Movies['imdb'])
			movie_links_scraper = movie_links_scraper()
			pDialog.update((index / num_shows) * 100, "Scraping Movie {} of {}".format(index, num_shows), Movies['title'])
			index += 1
			for links in movie_links_scraper:
				Scrapers_Run += 1
				pDialog.update((index / num_shows) * 100, "Scraping Movie {} of {}".format(index, num_shows), Movies['title'] + ' | '+str(int(Scrapers_Run))+'/'+str(len(No_of_scrapers)))	
		Scrapers_Run = 0
		if dialog.yesno("universalscrapers Testing Mode", 'Would you like to run a tv show?',
		tv_shows['title']+' ('+tv_shows['year']+') S'+tv_shows['season']+'E'+tv_shows['episode']):
			episode_links_scraper = universalscrapers.scrape_episode(tv_shows['title'], tv_shows['show_year'], tv_shows['year'], tv_shows['season'], tv_shows['episode'], tv_shows['imdb'],'')
			episode_links_scraper = episode_links_scraper()
			pDialog.update((index / num_shows) * 100, "Scraping TV Show {} of {}".format(index, num_shows), tv_shows['title'])
			index += 1
			for links in episode_links_scraper:
				Scrapers_Run += 1
				pDialog.update((index / num_shows) * 100, "Scraping TV Show {} of {}".format(index, num_shows), tv_shows['title'] + ' | '+str(int(Scrapers_Run))+'/'+str(len(No_of_scrapers)))	
		else:
			get_scraper_results()
			return
		count += 1
		single_test(count, index)
				
def full_test():
	index = 0
	pDialog.create('universalscrapers Testing mode active', 'please wait')
	for item in movies:
		Scrapers_Run = 0
		if pDialog.iscanceled():
			break
		movie_links_scraper = universalscrapers.scrape_movie(item['title'], item['year'], item['imdb'])
		movie_links_scraper = movie_links_scraper()
		pDialog.update((index / num_shows) * 100, "Scraping Movie {} of {}".format(index, num_shows), item['title'])
		index += 1
		for links in movie_links_scraper:
			Scrapers_Run += 1
			pDialog.update((index / num_shows) * 100, "Scraping Movie {} of {}".format(index, num_shows), item['title'] + ' | '+str(int(Scrapers_Run))+'/'+str(len(No_of_scrapers)))
	for item in shows:
		Scrapers_Run = 0
		if pDialog.iscanceled():
			break
		episode_links_scraper = universalscrapers.scrape_episode(item['title'], item['show_year'], item['year'], item['season'], item['episode'], item['imdb'],'')
		episode_links_scraper = episode_links_scraper()
		pDialog.update((index / num_shows) * 100, "Scraping TV Show {} of {}".format(index, num_shows), item['title'])
		index += 1
		for links in episode_links_scraper:
			Scrapers_Run += 1
			pDialog.update((index / num_shows) * 100, "Scraping TV Show {} of {}".format(index, num_shows), item['title'] + ' | '+str(int(Scrapers_Run))+'/'+str(len(No_of_scrapers)))
	get_scraper_results()
	
if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
# Universal Scrapers
import re
import time
import base64
import requests

import xbmcaddon

from ..scraper import Scraper
from ..common import (
    clean_title, clean_search, random_agent, filter_host, send_log, error_log
)

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting('dev_log') == 'true'


class darewatch(Scraper):
    domains = ['ondarewatch.com/', 'dailytvfix.com']
    name = "DareWatch"
    
    def __init__(self):
        self.base_link = 'http://www.dailytvfix.com/'
        self.search_url = self.base_link + 'ajax/search.php'
        self.ua = random_agent()
        self.sources = [ ]
        

    def _search_get_sources(self, search_id, title, year, season, episode, is_movie):
        # Search headers tuned for 'http://www.dailytvfix/ajax/search.php'.
        search_headers = {
            'Host': self.base_link.replace('http://', '', 1)[:-1],
            'User-Agent': self.ua,
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': self.base_link,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive'
        }
        data = {'limit': 15, 'q': search_id, 'timestamp': int(time.time() * 1000)}
        mediatype = 'movie' if is_movie else 'tv'
        
        start_time = time.time()
        
        r = requests.post(self.search_url, data=data, headers=search_headers, timeout=8)
        if r.ok and r.text != 'Restricted access':
            page_url = None
            
            if is_movie:
                for entry in r.json():
                    entry_title = entry['title'].lower()
                    if mediatype in entry['meta'].lower() and (entry_title == search_id or entry_title == title.lower()):
                        page_url = self.base_link + entry['permalink']
                        break
            else:
                best_sources = [ ]
                for entry in r.json():
                    if mediatype in entry['meta'].lower():
                        entry_title = entry['title'].lower()
                        if entry_title == search_id:
                            best_sources.append(entry['permalink'])
                        elif ((search_id in entry_title or title.lower() in entry_title) and year in entry_title):
                            # For special cases like 'The Flash' vs 'The Flash 2014', make the entry
                            # that matches the most (including year) be prepended.
                            best_sources.insert(0, entry['permalink'])                            
                if best_sources:
                    page_url = self.base_link + best_sources[0] + '/season/%s/episode/%s' % (season, episode)
            
            if page_url:
                self.get_sources(page_url, title, year, season, episode, start_time)
        else:
            if dev_log:
                error_log(self.name, '%s %s' % (r, r.text))
                
        if dev_log:
            elapsed = time.time() - start_time
            send_log(self.name, elapsed, len(self.sources), title, year, season=season, episode=episode)
        return self.sources


    def scrape_movie(self, title, year, imdb, debrid=False):
        try:            
            return self._search_get_sources(clean_search(title), title, year, '', '', is_movie=True)

        except Exception, argument:
            if dev_log:
                error_log(self.name,argument)
            return [ ]

        
    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            return self._search_get_sources(clean_search(title), title, show_year, season, episode, is_movie=False)

        except Exception, argument:
            if dev_log:
                error_log(self.name,argument)
            return [ ]


    def get_sources(self, item_url, title, year, season, episode, start_time):
        try:
            r = requests.get(item_url, headers={'User-Agent': self.ua}, timeout=10)
            if not r.ok:
                return
           
            match = re.findall("] = '(.+?)'", r.text, re.DOTALL)
            for vid in match:
                iframe = base64.b64decode(vid)
                temp = re.findall('src="(.+?)"', iframe, re.DOTALL|re.IGNORECASE)
                if temp:
                    host_url = temp[0].strip() # strip() because sometimes there's an '\r' at the end.
                else:
                    continue                    
                
                if 'openload' in host_url:
                    try:
                        openload_page = requests.get(host_url, headers=headers, timeout=8).text
                        rez = re.compile('description" content="(.+?)"', openload_page, re.DOTALL|re.IGNORECASE)[0]
                        qual = '1080p' if '1080' in rez else '720p' if '720' in rez else 'SD'
                    except:
                        qual='SD'
                    self.sources.append(
                        {'source': 'Openload', 'quality': qual, 'scraper': self.name, 'url': host_url, 'direct': False}
                    )
                else:
                    hoster = host_url.split('//')[1].replace('www.', '', 1)
                    hoster = hoster[ : hoster.find('/')].lower()
                    if not filter_host(hoster):
                        continue
                    self.sources.append(
                        {'source': hoster, 'quality': 'DVD', 'scraper': self.name, 'url': host_url, 'direct': False}
                    )
        except:
            return
        
        
    def _debug(self, name, val):
        import xbmc
        xbmc.log('DAREWATCH > %s %s' % (name, str(val)), xbmc.LOGWARNING)

# -*- coding: utf-8 -*-
# Universal Scrapers checked 24/08/2018

import requests, re, time
import urllib, urlparse, json
import xbmcaddon
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_search, clean_title, send_log, error_log
from universalscrapers.modules import client, jsunpack, dom_parser, quality_tags

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

                                           
class watch32(Scraper):
    domains = ['watch32hd.co']
    name = "Watch32hd"
    sources = []

    def __init__(self):
        self.base_link = 'https://watch32hd.co'
        self.search_link = 'results?q=%s'

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time() 
            search_id = clean_search(title.lower())
            start_url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(search_id))
            headers={'User-Agent': client.agent()}
            html = client.request(start_url, headers=headers)
            results = client.parseDOM(html, 'div', attrs={'class': 'video_title'})

            items = []
            for item in results:
                try:
                    data = dom_parser.parse_dom(item, 'a', req=['href', 'title'])[0]
                    t = data.content
                    y = re.findall('\((\d{4})\)', data.attrs['title'])[0]
                    qual = data.attrs['title'].split('-')[1]
                    link = data.attrs['href']

                    if not clean_title(t) == clean_title(title): continue
                    if not y == year: continue

                    items += [(link, qual)]

                except:
                    pass
            for item in items:
                count = 0
                try:
                    url = item[0] if item[0].startswith('http') else urlparse.urljoin(self.base_link, item[0])
                    r = client.request(url)

                    qual = client.parseDOM(r, 'h1')[0]
                    res = quality_tags.get_release_quality(item[1], qual)[0]

                    url = re.findall('''frame_url\s*=\s*["']([^']+)['"]\;''', r, re.DOTALL)[0]
                    url = url if url.startswith('http') else urlparse.urljoin('https://', url)
                    if 'vidlink' in url:
                        html = client.request(url, headers=headers)
                        action = re.findall("action'\s*:\s*'([^']+)", html)[0]
                        postID = re.findall("postID\s*=\s*'([^']+)", html)[0]
                        url = 'https://vidlink.org' + re.findall("var\s*url\s*=\s*'([^']+)", html)[0]
                        data = {'browserName': 'Firefox',
                                'platform': 'Win32',
                                'postID': postID,
                                'action': action}

                        headers['X-Requested-With'] = 'XMLHttpRequest'
                        headers['Referer'] = url
                        html = client.request(url, post=data, headers=headers)
                        html = jsunpack.unpack(html).replace('\\', '')
                        sources = json.loads(re.findall('window\.srcs\s*=\s*([^;]+)', html, re.DOTALL)[0])
                        for src in sources:
                            r = requests.head(src['url'], headers={'User-Agent': client.agent()})
                            if r.status_code < 400:
                                movie_link = src['url']
                                count += 1
                                self.sources.append({'source': 'Googlelink', 'quality': res,
                                                    'scraper': self.name, 'url': movie_link, 'direct': True})
                            else:
                               continue

                except:
                    pass
                if dev_log=='true':
                    end_time = time.time() - start_time
                    send_log(self.name,end_time, count, title,year)
            #print self.sources
            return self.sources
        except Exception, argument:
            print argument
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

#watch32().scrape_movie('Black Panther', '2018', 'tt1825683', False)
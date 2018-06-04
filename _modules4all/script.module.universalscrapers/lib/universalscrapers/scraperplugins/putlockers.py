import requests,re,time
import urllib, base64
from ..jsunpack import unpack
import xbmcaddon
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

a = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
b = requests.Session()
c = {'User-Agent':a}
                                           
class putlockers(Scraper):
    domains = ['putlockers-hd.stream']
    name = "Putlockers"
    headache = []
 
    def __init__(self):
        self.i = 'https://putlockers-hd.stream'

    def scrape_movie(self, x, y, z, debrid = False):
        try:
            count = 0
            start_headache = time.time() 
            e = clean_search(x.lower())
            l = '%s/?s=%s+%s' %(self.i,e.replace(' ','+'),y)
#            print l
            i = b.get(l,headers=c,timeout=5).content
            f = re.findall('<div class="thumbnail animation-2">.+?href="(.+?)">.+?alt="(.+?)"',i)
            for e, l in f:
                d, g = re.findall('(.+?)\((.+?)\)',str(l))[0]
                if clean_title(d) == clean_title(x) and g == y:
 #                   print e
                    q = b.get(e).content
                    r = re.findall('<iframe class="metaframe rptss" src="(.+?)"',q)[0]
                    t = b.get(r).content
                    u = re.findall("var tc = '(.+?)'.+?url: \"(.+?)\".+?\"_token\": \"(.+?)\".+?function.+?\(s\)(.+?)</script>",t,re.DOTALL)
                    for v, w, xoxo, yoyo in u:
                        o = self.get_x_token(v,yoyo)
                        p = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
                                   'Host':'gomostream.com',
                                   'Referer':r,
                                   'x-token':o}
                        g = {'tokenCode':v,
                                '_token':xoxo}
                        l = b.post(w,headers=p,data=g).json()
                        for a in l:
                            if 'putvid' in a:
                                z = b.get(a).content
                                enjoy = re.findall("<script type='text/javascript'>(.+?)</script>",z,re.DOTALL)[0]
                                enjoy = unpack(enjoy)
                                enjoy = re.findall('sources:\["(.+?)"',str(enjoy))[0]
                                count+=1
                                self.headache.append({'source': 'Putvid', 'quality': 'Unknown - Probably good', 'scraper': self.name, 'url': enjoy,'direct': False})
                            elif 'openload' in a or 'streamango' in a:
                                if 'openload' in a:
                                    something = 'Openload'
                                elif 'streamango' in a:
                                    something = 'Streamango'
                                z = b.get(a).content
                                fun = re.findall('"description" content="(.+?)"',z)[0]
                                if '1080p' in fun:
                                    somestuff = '1080p'
                                elif '720p' in fun:
                                    somestuff = '720p'
                                else:
                                    somestuff = 'SD'
                                count+=1
                                self.headache.append({'source': something, 'quality': somestuff, 'scraper': self.name, 'url': a,'direct': False})
                if dev_log=='true':
                    end_it_all = time.time() - start_headache
                    send_log(self.name,end_it_all,count,x,y)   
            return self.headache
        except Exception, argument:
            print argument
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

    def get_x_token(self,ta,xb):
        st,fi,a1,a2 = re.findall('slice\((.+?),(.+?)\).+?\+ "(.+?)"\+"(.+?)"',str(xb))[0]
        split = ta[int(st):int(fi)]
        rev = split[::-1]
        to = str(rev)+a1+a2
        return to


#putlockerhd().scrape_movie('logan','2017','')

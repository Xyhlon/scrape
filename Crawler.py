import re
import threading
import time
import urllib.parse
from itertools import chain

from lxml.etree import tostring
from requests import Session
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from Downloader import Downloader
from extractor import Extractor
from interactor.Interactor import Interactor
from mongocache import MongoCache
import seleniumwire.webdriver

# from mulitprocess import multiprocess
# from pprint import pprint
# import multiprocessing

USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
Type = 1
Cache = 'what'
DiskCache = 1
proxs = ['http://172.29.255.254:800']


class Crawler:
    def __init__(self, threaded=True, useragent=USERAGENT, cache=None, delay=5, proxies=None, retries=1, threads=20,
                 rest=20, extractor=Extractor()):
        self.agent = useragent
        self.threaded = threaded
        self.delay = delay
        self.proxies = proxies
        self.retries = retries
        self.rest = rest
        self.threads = threads
        self.extractor = extractor
        self.cache = MongoCache() if threaded is True else cache
        self.downloader = Downloader(user_agent=self.agent, delay=self.delay, proxies=self.proxies,
                                     retries=self.retries,
                                     rest=self.rest, cache=self.cache)

    def linkcrawler(self, seedurl, urlfilter='supremenewyork'):
        if isinstance(self.cache, MongoCache):
            # print('is mongo')
            self.cache.clear()
            # self.cache.status()
            self.cache.push(seedurl)
            # self.cache.status()
            while True:
                try:
                    url = self.cache.pop()
                    # self.cache.status()
                except KeyError:
                    break
                else:
                    html = self.downloader(url, 'selenium')
                    if url is None:
                        print('URL is None')
                    if self.extractor:
                        try:
                            links = self.extractor(url, html, urlfilter, 'a') or []
                        except Exception as e:
                            print('Error in Extraction ' + str(url) + ' ' + str(e))
                        else:
                            for link in links:
                                # reformulate defrag links
                                # self.cache.status()
                                if link is not None and link.get('href') is not None:
                                    new_url = self.normalize(url, link.get('href'))
                                    if re.search(urlfilter, new_url):
                                        # print(new_url)
                                        self.cache.push(new_url)
                    self.cache.done(url)

        elif self.cache is DiskCache:
            self.cache.__setitem__()
        else:
            self.cache = [seedurl]

    def crawlloop(self, urlfilter, pop, push, done):
        while True:
            try:
                url = pop()
                # self.cache.status()
            except KeyError:
                break
            else:
                html = self.downloader(url, 'selenium')
                if url is None:
                    print('URL is None')
                if self.extractor:
                    try:
                        links = self.extractor(url, html, urlfilter, 'a') or []
                    except Exception as e:
                        print('Error in Extraction ' + str(url) + ' ' + str(e))
                    else:
                        for link in links:
                            # reformulate defrag links
                            # self.cache.status()

                            if link is not None and link.get('href') is not None:
                                # print(link.get('href'))
                                new_url = self.normalize(url, link.get('href'))
                                if re.search(urlfilter, new_url):
                                    # print(new_url)
                                    push(new_url)
                done(url)

    # @multiprocess
    def parallelcrawler(self, seedurl):
        self.cache.clear()
        self.cache.push(seedurl)
        self.crawlloop('supremenewyork.com/', self.cache.pop, self.cache.push, self.cache.done)

    @staticmethod
    def normalize(referer, link):
        if 'http' in link:
            return link
        else:
            link, _ = urllib.parse.urldefrag(link)
            parts = urllib.parse.urlparse(referer)
            # deal external link
            # if parts.netloc is not
            # domain
            baseurl = parts.scheme + '://' + parts.netloc
            return urllib.parse.urljoin(baseurl, link)

    # crawlsetup
    # single
    def pocessablecrawler(self, scope):
        threads = []
        while threads or self.cache.still():
            # print(len(threads))
            # print(self.cache.still())
            for thread in threads:
                if not thread.is_alive():
                    threads.remove(thread)
            while len(threads) < self.threads and self.cache.check():
                thread = threading.Thread(
                    target=self.crawlloop, args=(scope, self.cache.pop, self.cache.push, self.cache.done))
                thread.setDaemon(True)
                thread.start()
                threads.append(thread)
            time.sleep(0)

    def crawlsetup(self, seedurl):
        self.cache.clear()
        self.cache.push(seedurl)

    def fastload(self, url, headers=None, *args, **kwargs):
        d = Downloader()
        # 'form[target] [name]'
        i = Interactor(selector='form [name]')
        if 'selenium' in args or kwargs:
            if 'firefox' in args or kwargs:
                options = Options()
                options.headless = True
                drive = webdriver.Firefox(options=options)
            else:
                drive = webdriver.PhantomJS()
            # html = d.selload(drive, url)
            html = d(url)
            formdata = i.formdata(html, i.selector)
            # formdata = i.formdata(html['html'], i.selector)
            i.select('Large')
            d.selpost(drive, url, i.data['data'])
            print(drive.page_source)
            # is important to wait before closing the drive the whole drive
            if drive.page_source:
                drive.close()
        else:
            s = Session()
            html = s.get(url)
            print(html.headers)
            data = i.formdata(html.text, selector=i.selector)
            # action link print(data['action'])
            action = self.normalize(url, data['action'])
            # action url print(action)
            print(action)
            i.select('Large')
            print(i.data['data'])
            print(s.cookies.get_dict())
            cookies = s.cookies.get_dict()

            resp = d.postload(s, referer=url, action=action, data=i.data['data'], cookies=cookies)
            # status code of post print(resp['code'])
            print(s.cookies.get_dict())
            print(resp['resp'].request.headers)
            print(resp['resp'].cookies)
            print(resp['html'])
            s.close()




def stringify_children(node):
    parts = ([node.text] +
             list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) +
             [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))


dusch = Crawler(threaded=True)
# dusch.linkcrawler('https://www.supremenewyork.com/shop')
# dusch.crawlsetup('https://www.supremenewyork.com/shop')
# dusch.crawlsetup('http://www.gym-kirchengasse.at/')
# dusch.pocessablecrawler('gasse.at/')
# cursor = dusch.cache.db.webpage.find()
# for document in cursor:
#    pprint(document)

# dusch.fastload('https://www.w3schools.com/html/html_forms.asp', None)
dusch.fastload('https://www.supremenewyork.com/shop/jackets/d5vdqbxi1/e1jr3mahu', None, 'selenium', 'firefox')
# for c in dusch.cache.db.webpage.find():
#   pprint(c)
# if __name__ == '__main__':
#    dusch.parallelcrawler('https://www.supremenewyork.com/shop')
# dusch.cache.status()
# print(url)
# choose random user-agent from list of user-agents

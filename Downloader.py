import datetime
import random
import socket
import time
import urllib
import urllib.request

from requests import Request
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

UserAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
RETRIES = 1
DELAY = 1
REST = 20


class Downloader:
    def __init__(self, delay=DELAY, user_agent=UserAgent, proxies=None, retries=RETRIES, rest=REST, opener=None,
                 cache=None, headers=None):
        socket.setdefaulttimeout(rest)
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.retries = retries
        self.opener = opener
        self.cache = cache
        self.headers = headers

    def __call__(self, url, *args, **kwargs):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                pass
            else:
                if self.retries > 0 and 500 <= result['code'] < 600:
                    result = None
        if result is None:
            # self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = kwargs.get('headers') if 'headers' in kwargs else {'User-agent': self.user_agent}
            if 'selenium' in args:
                result = self.selload(url)
            else:
                result = self.download(url, headers, proxy=proxy, retries=self.retries)
            if self.cache:
                self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxy, retries, data=None):
        request = urllib.request.Request(url, data, headers)
        opener = self.opener or urllib.request.build_opener()
        if proxy:
            params = {urllib.parse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib.request.ProxyHandler(params))
        try:
            response = opener.open(request)
            html = response.read()
            code = response.code
        except Exception as e:
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if retries > 0 and 500 <= code < 600:
                    return self._get(url, headers, proxy, retries - 1, data)
            else:
                code = None
        return {'html': html, 'code': code}

    def postload(self, session, referer, action, data, proxies=None, **kwargs):
        req = Request('POST', action, data=data, headers={'Referer': referer, 'User-agent': UserAgent}, **kwargs)
        prepped = req.prepare()
        resp = session.send(prepped, proxies=proxies)
        return {'html': resp.text, 'code': resp.status_code, 'resp': resp}

    def selpost(self, driver, url, data, *args, **kwargs):
        driver.implicitly_wait(3)
        driver.get(url)
        for key in data:
            field = driver.find_element_by_css_selector("form [name={}]".format(key))
            # print(elements[0].attrib['name'])
            # print(elements[0].tag_name)
            # field = elements[0]
            if field.tag_name in 'select':
                option = field.find_element_by_css_selector("[value='{}']".format(data[key]))
                # print(option.tag_name)
                option.click()
                # tag = driver.find_element_by_xpath(
                #     "//select[name={}]/option[value={}]".format(key, data[key]))
                # print(tag.tag_name)
            else:
                if field.get_attribute("type") not in 'hidden submit':
                    field.clear()
                    field.send_keys(data[key])
        submit = driver.find_elements_by_css_selector("form [type=submit]")
        submit[0].click()
        if 'tab' in args or kwargs:
            WebDriverWait(driver, 10).until(
                EC.number_of_windows_to_be(2)
            )
            child = driver.window_handles[1]
            driver.close()
            driver.switch_to_window(child)

    def selload(self, driver, url, *args, **kwargs):
        driver.implicitly_wait(3)
        driver.get(url)
        html = driver.page_source
        # response = webdriver.request('POST', 'url here', data=)
        # TODO: return drive and declare drive in crawler and not close drive
        return {'html': html}

    def wirepost(self, driver, url, data, *args, **kwargs):
        driver.implicitly_wait(3)
        gotta = driver.get(url)
        print(gotta.request)
        for key in data:
            field = driver.find_element_by_css_selector("form [name={}]".format(key))
            if field.tag_name in 'select':
                option = field.find_element_by_css_selector("[value='{}']".format(data[key]))
                option.click()
            else:
                if field.get_attribute("type") not in 'hidden submit':
                    field.clear()
                    field.send_keys(data[key])
        submit = driver.find_elements_by_css_selector("form [type=submit]")
        submit[0].click()
        if 'tab' in args or kwargs:
            WebDriverWait(driver, 10).until(
                EC.number_of_windows_to_be(2)
            )
            child = driver.window_handles[1]
            driver.close()
            driver.switch_to_window(child)

class Throttle:
    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        domain = urllib.parse.urlparse.urlsplit(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleepfor = self.delay - (datetime.now() - last_accessed).seconds
            if sleepfor > 0:
                time.sleep(sleepfor)
        self.domains[domain] = datetime.now()

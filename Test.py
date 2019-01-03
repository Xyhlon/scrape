import lxml.html
import bs4
import urllib.request
import lxml.cssselect

def download(URL):
    html = urllib.request.urlopen(URL).read()
    tree = lxml.html.fromstring(html)
    return tree


def filter(html, filt, num=0):
    precious = html.cssselect(filt)[num]
    print(precious)
    return precious


webpage = 'https://www.supremenewyork.com/shop/all'
site = 'https://www.google.com'
dump = download(webpage)
# neet = filter(dump, 'form.tsf nj')
neet = filter(dump, 'ul#nav-categories > li > a')
# form#tsf > input
print(neet.text_content())

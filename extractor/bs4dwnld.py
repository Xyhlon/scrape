import urllib
from urllib import request
from bs4 import BeautifulSoup as Soup


def download(url):
    # get the html
    text = urllib.request.urlopen(url).read()
    # parses the html and makes it a BS4 object
    html = Soup(text, 'html.parser')
    # prints the title tag
    print(html.title)
    # finds all li tags with the id footer-info-lastmod
    print(html.findAll('li', id="footer-info-lastmod"))
    # how to use the structure
    print(html.body.div['id'])
    # for further documentation visit https://www.crummy.com/software/BeautifulSoup/bs4/doc/


# initialize the download
download('https://en.wikipedia.org/wiki/Power_(physics)')
download('https://en.wikipedia.org/wiki/O_Tannenbaum')

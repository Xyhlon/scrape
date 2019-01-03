import lxml.cssselect
import lxml.html
import urllib
from urllib import request


def download(url):
    # get the html
    text = urllib.request.urlopen(url).read()
    tree = lxml.html.fromstring(text)
    # search for div tags beneath a body
    divs = tree.cssselect('body div:nth-child(1)')
    # display all attributes of the divs found
    for div in divs:
        print(div.attrib)
    # take the first div and display its text
    print(divs[1].text)


download('https://en.wikipedia.org/wiki/Power_(physics)')
download('https://en.wikipedia.org/wiki/O_Tannenbaum')

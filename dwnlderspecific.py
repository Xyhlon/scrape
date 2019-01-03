# first it is necessary to import the downloader
# for that the urllib module is used
import urllib.request


# next a function is defined which downloads the givens URLs html page
# using the imported module
def download(url):
    text = urllib.request.urlopen(url).read()
    return text

# print(download('https://en.wikipedia.org/wiki/Power_(physics)'))

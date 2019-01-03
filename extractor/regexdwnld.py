import re
import urllib
from urllib import request

fiveletter = re.compile("\s\w\w\w\w\w\s")
timepat = re.compile("\d\d:\d\d")
datepat = re.compile("\d\d\.\d\d\.\d\d\d\d")


def download(url):
    text = str(urllib.request.urlopen(url).read())
    print(datepat.findall(text))
    print(fiveletter.findall(text))
    print(timepat.findall(text))


download('https://en.wikipedia.org/wiki/Power_(physics)')
download('https://en.wikipedia.org/wiki/O_Tannenbaum')

# download('https://www.timeanddate.com/worldclock/timezone/utc')
# download('https://time.is/UTC')
# opener = urllib.request.build_opener()
# req = request.Request(url, headers={
#    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'})
# text = str(opener.open(req).read()
# datepattern = re.compile(
#    '^((((0[13578])|([13578])|(1[02]))[.\:/](([1-9])|([0-2][0-9])|(3[01])))|(((0[469])|([469])|(11))[.\:/](([1-9])|([0-2][0-9])|(30)))|((2|02)[.\:/](([1-9])|([0-2][0-9]))))[\/]\d{4}$|^\d{4}$')
# timepattern = re.compile('^([0-1][0-9]|[2][0-3]):([0-5][0-9])$')
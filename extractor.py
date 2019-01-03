import re

import lxml.cssselect
import lxml.html


class Extractor:
    def __init__(self, method=None):
        self.method = method

    def __call__(self, url, html, urlfilter, selector, *args, **kwargs):
        if re.search(urlfilter, url):
            tree = lxml.html.fromstring(html)
            tags = tree.cssselect(selector)
            return tags

# ex = Extractor()
# er = ex('https://docs.mongodb.com/',
#   '<title>Supreme</title><meta content="Supreme. The official website of Supreme. EST 1994. NYC." name="description" /><meta content="telephone=no" name="format-detection" /><meta content="on" http-equiv="cleartype" /><meta content="notranslate" name="google" /><meta content="app-id=664573705" name="apple-itunes-app" /><link href="//www.google-analytics.com" rel="dns-prefetch" /><link href="//ssl.google-analytics.com" rel="dns-prefetch" /><link href="//d2flb1n945r21v.cloudfront.net" rel="dns-prefetch" /><script src="https://www.google.com/recaptcha/api.js">async defer</script><meta content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1, user-scalable=no" id="viewport" name="viewport" /><link rel="stylesheet" media="all" href="//d17ol771963kd3.cloudfront.net/assets/application-0104cafa9f885ad3f4ddb3939644e936.css" /><script type="text/javascript">window.supremetohru = "1cda301447ea90d9d14e0a382296f22fec3b1d0da474a27ac628a946858a12480fb1d0a7aee102f237859f1a8c28ad6745e63f1e2169dc29c94064c8b5380194";</script><script src="//d17ol771963kd3.cloudfront.net/assets/pooky.min.0c81000b8c6d2e1c849b.js"></script><meta name="csrf-param" content="authenticity_token" />',
#   '', 'title')
# print(er[0].text_content())

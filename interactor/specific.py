import urllib.request

import lxml.html
from requests import Session


def getdata(html):
    tree = lxml.html.fromstring(html)
    formdata = {}
    for input in tree.cssselect('form input'):
        formdata[input.attrib['name']] = input.attrib['value']

    for select in tree.cssselect('form select'):
        options = []
        for option in select:
            options.append(option.attrib['value'])

        formdata[select.attrib['name']] = options

    form = tree.cssselect('form')[0]
    action = form.attrib['action']
    method = form.attrib['method']
    return {'data': formdata, 'action': action, 'method': method}

    # for form in tree.cssselect('form'):
    #     print(form.attrib['action'] + '\t' + form.attrib['method'])


def download(url):
    text = urllib.request.urlopen(url).read()
    return text


def usedata(url):
    session = Session()
    session.head('https://www.supremenewyork.com/shop/')
    html = download(url)
    poststuff = getdata(html)
    response = session.post(url='https://www.supremenewyork.com/' + poststuff['action'], data=poststuff['data'],
                            headers={'Referer': url})
    print(response.text)
    check = session.get('https://www.supremenewyork.com/shop/')
    tree = lxml.html.fromstring(check.text)
    print(tree.cssselect('div#cart')[0].attrib)


#usedata('https://www.supremenewyork.com/shop/jackets/e48qbfopx/tyh9ez3pi')

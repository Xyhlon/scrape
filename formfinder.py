import urllib.request
import lxml.html

import lxml


def download(url):
    text = urllib.request.urlopen(url).read()
    tree = lxml.html.fromstring(text)
    tags = tree.cssselect('form [name]')
    formdata = {}
    for tag in tags:
        key = tag.attrib['name']
        if tag.tag == 'select':
            options = []
            for option in tag:
                options.append(option.attrib['value'])
            value = options
        else:
            if 'value' in tag.attrib:
                if tag.type not in 'text':
                    value = tag.attrib['value']
                else:
                    value = tag.type
            else:
                if 'type' in tag.attrib:
                    value = tag.type
                else:
                    value = None
        formdata[key] = value
    print(formdata)
    # print(tag)
    # if tag.attrib['name'] is not None:
    #     print(tag.attrib['name'] + '\t' + tag.attrib['value'])
    # else:
    #     print(tag.attrib['value'])


download('https://www.supremenewyork.com/shop/accessories/hmlor31jx/mj8tuf3as')
download('http://aavtrain.com/')
download('https://www.supremenewyork.com/shop/sweatshirts/h6xhk924g/mrj0p8keh')
download('https://www.roboform.com/filling-test-all-fields')
download('https://www.w3schools.com/html/html_forms.asp')
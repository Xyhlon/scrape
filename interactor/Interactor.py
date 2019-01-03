import lxml
import lxml.html
from requests import Session
import re
from dwnlderspecific import download


class Interactor:
    def __init__(self, selector='form [name]'):
        self.data = None
        self.url = None
        self.base = None
        self.tree = None
        self.selector = selector

    def formdata(self, html, selector):
        tree = lxml.html.fromstring(html)
        self.tree = tree
        tags = tree.cssselect(selector)
        formdata = {}
        for tag in tags:
            key = tag.attrib['name']
            if tag.tag == 'select':
                options = {}
                for option in tag:
                    options[option.text] = option.attrib['value']
                value = options
            else:
                if 'value' in tag.attrib:
                    if tag.type not in 'text':
                        preval = tag.attrib['value']
                        value = re.sub("\s+", "+", preval.strip())
                    else:
                        value = tag.type
                else:
                    if 'type' in tag.attrib:
                        value = tag.type
                    else:
                        value = None
            formdata[key] = value
            parent = tag.getparent()
            if parent.tag == 'form':
                attr = parent.attrib
                if 'method' in attr and 'action' in attr:
                    action = parent.attrib['action']
                    method = parent.attrib['method']
                elif 'method' in attr:
                    method = parent.attrib['method']
                    action = ''
                elif 'action' in attr:
                    action = parent.attrib['action']
                    method = 'post'
        # print(formdata)
        self.data = {'data': formdata, 'action': action, 'method': method}

        return {'data': formdata, 'action': action, 'method': method}

    def submit(self, base, html, url):
        self.base = base
        self.url = url
        formdata = self.formdata(html, self.selector)
        self.select('Medium')
        # print(self.data)
        session: Session = Session()
        session.head(url)
        if formdata['method'] == 'post':
            response = session.post(url=base + formdata['action'], data=self.data['data'], headers={'Referer': url})
            # print(response.text)
            print(response.status_code)
            return session
        elif formdata['method'] == 'get':
            response = session.get(url, data=formdata['data'])
            # print(response.text)
            print(response.status_code)
            return session

    def select(self, *args, **kwargs):
        for key in self.data['data']:
            stuff = self.data['data'][key]
            if isinstance(stuff, dict):
                try:
                    wanted = 'err'
                    if args:
                        for arg in args:
                            # print(stuff)
                            if arg in self.data['data'][key]:
                                wanted = stuff[arg]
                    if kwargs:
                        for kwarg in kwargs:
                            if kwarg in self.data['data'][key]:
                                wanted = stuff[kwarg]
                    self.data['data'][key] = wanted
                except UnboundLocalError as ue:
                    print(ue)

# boi = Interactor()

# html = download('https://www.supremenewyork.com/shop/jackets/e48qbfopx/tyh9ez3pi')
# boi.submit('https://www.supremenewyork.com/', url='https://www.supremenewyork.com/shop/jackets/e48qbfopx/tyh9ez3pi',
#           html=html)
# boi2 = Interactor(selector='form[target] [name]')
# html = download('https://www.w3schools.com/html/html_forms.asp')
# boi2.submit('https://www.w3schools.com', html, 'https://www.w3schools.com/html/html_forms.asp')

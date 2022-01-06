import requests
import time, re

username = "ԱշբոտՏՆՂ"
password = "TeokratakanAratta28dbc"
S = requests.Session()


class Page:
    def __init__(self, wiki, title, ns=None):
        self.wiki = wiki
        if isinstance(ns, str):
            self.ns = wiki.nsMap[ns]
        else:
            self.ns = ns
        self.title = title
        self.sitelinks = None
        self.item = None    

    def __str__(self):
        return '[[:' + str(self.wiki.lang) + ":" + str(self.title) + ']]'

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.__dict__ == other.__dict__

    def exists(self):
        data = self.wiki.apiRec({
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "titles": self.title
        })
        if 'query' in data and '-1' in data['query']['pages']:
            self.exist = False
            return False
        else:
            self.exist = True
            return True

    def getNs(self):
        if self.ns:
            return self.ns
        query = self.wiki.getQuery({
            "prop": "pageprops",
            "titles": self.title,
        }, "pages", "pp")

        for id in query[0]:
            self.ns = query[0][id]['ns']
            break
        return self.ns

    def getItem(self):
        if self.wiki.project == 'wikidata':
            return self
        if self.item:
            return self.item
        query = self.wiki.getQuery({
            "prop": "pageprops",
            "titles": self.title,
        }, "pages", "pp")
        Q = ""
        for id in query[0]:
            if id == '-1':
                return None
            elif 'pageprops' not in query[0][id] or 'wikibase_item' not in query[0][id]['pageprops']:
                return None
            Q = query[0][id]['pageprops']['wikibase_item']
            break
        self.item = Page(Wiki('wikidata', 'wikidata'), Q, 0)
        return self.item

    def getSiteLinks(self):
        if self.sitelinks:
            return self.sitelinks
        item = self.getItem()
        if not item:
            return None
        data = item.wiki.apiRec({
            "action": "wbgetentities",
            "format": "json",
            "ids": item.title,
            "props": "sitelinks"
        })
        sitelinks = {}
        if 'entities' not in data or item.title not in data['entities'] or 'sitelinks' not in data['entities'][
            item.title]:
            return None

        for sitelink in data['entities'][item.title]['sitelinks']:
            if 'wiktionary' in sitelink:
                lang, project = sitelink.split('wiktionary')
                project = 'wiktionary'
            else:
                lang, project = sitelink.split('wiki', 1)
            if project == '':
                project = 'pedia'
            project = 'wiki' + project
            sitelinks[lang + project] = Page(Wiki(lang, project),
                                             data['entities'][item.title]['sitelinks'][sitelink]['title'])
        self.sitelinks = sitelinks
        return sitelinks

    def convertTo(self, toWiki):
        if toWiki.project == 'wikidata':
            return self.getItem()
        item = self.getItem()
        if not item:
            return None
        if not self.sitelinks:
            self.sitelinks = item.getSiteLinks()
        if self.sitelinks and toWiki.lang + toWiki.project in self.sitelinks:
            return self.sitelinks[toWiki.lang + toWiki.project]
        else:
            return None

    def size(self):
        get = self.wiki.apiRec({
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "titles": self.title,
            "rvprop": "size"
        })
        if 'query' in get:
            for page in get['query']['pages']:
                if 'revisions' in get['query']['pages'][page]:
                    return get['query']['pages'][page]['revisions'][0]['size']
                else:
                    return 0

    def read(self):
        pages = self.wiki.apiRec({
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "titles": self.title,
            "rvprop": "content",
            "rvslots": "*"
        })['query']['pages']
        for page in pages:
            if 'revisions' in pages[page] and 'slots' in pages[page]['revisions'][0] and 'main' in \
                    pages[page]['revisions'][0]['slots']:
                return pages[page]['revisions'][0]['slots']['main']['*']

    def getCSRF(self):
        return self.wiki.apiRec({
            "action": "query",
            "meta": "tokens",
            "format": "json"
        })["query"]["tokens"]["csrftoken"]

    def save(self, text):
        return S.post(self.wiki.api, {
            "action": "edit",
            "format": "json",
            "title": self.title,
            "text": text,
            "token": self.getCSRF()
        })

    def categories(self, hidden=None):
        if hidden:
            clshow = hidden
        else:
            clshow = ""
        data = self.wiki.getQuery({
            "prop": "categories",
            "titles": self.title,
            "clshow": clshow
        }, 'pages', 'cl')
        cats = []
        for b in data:
            for i in b:
                if 'categories' in b[i]:
                    for cat in b[i]['categories']:
                        cats.append(cat['title'])
        return cats


class Wiki:
    nsMap = {
        0: "",
        1: "Talk",
        2: "User",
        3: "User talk",
        4: "Wikipedia",
        5: "Wikipedia talk",
        6: "File",
        7: "File talk",
        8: "MediaWiki",
        9: "MediaWiki talk",
        10: "Template",
        11: "Template talk",
        12: "Help",
        13: "Help talk",
        14: "Category",
        15: "Category talk",
        100: "Portal",
        101: "Portal talk",
        108: "Book",
        109: "Book talk",
        118: "Draft",
        119: "Draft talk",
        446: "Education Program",
        447: "Education Program talk",
        710: "TimedText",
        711: "TimedText talk",
        828: "Module",
        829: "Module talk",
        2300: "Gadget",
        2301: "Gadget talk",
        2302: "Gadget definition",
        2303: "Gadget definition talk",
        -2: "Media",
        -1: "Special",
        "": 0,
        "Talk": 1,
        "User": 2,
        "User talk": 3,
        "Wikipedia": 4,
        "Wikipedia talk": 5,
        "File": 6,
        "File talk": 7,
        "MediaWiki": 8,
        "MediaWiki talk": 9,
        "Template": 10,
        "Template talk": 11,
        "Help": 12,
        "Help talk": 13,
        "Category": 14,
        "Category talk": 15,
        "Portal": 100,
        "Portal talk": 101,
        "Book": 108,
        "Book talk": 109,
        "Draft": 118,
        "Draft talk": 119,
        "Education Program": 446,
        "Education Program talk": 447,
        "TimedText": 710,
        "TimedText talk": 711,
        "Module": 828,
        "Module talk": 829,
        "Gadget": 2300,
        "Gadget talk": 2301,
        "Gadget definition": 2302,
        "Gadget definition talk": 2303,
        "Media": -2,
        "Special": -1
    }

    def __init__(self, lang, project):
        self.lang = lang
        self.project = project
        self.api = 'https://{}.{}.org/w/api.php?'.format(lang, project)
        if lang == 'wikidata':
            self.api = 'https://wikidata.org/w/api.php?'
        # self.login()

    def __str__(self):
        return str(self.lang) + ":" + str(self.project)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.__dict__ == other.__dict__

    def login(self):
        loginToken = self.apiRec({
            "action": "query",
            "meta": "tokens",
            "format": "json",
            "type": "login"
        })["query"]["tokens"]["logintoken"]
        S.post(self.api, {
            "action": "login",
            "format": "json",
            "lgname": username,
            "lgpassword": password,
            "lgtoken": loginToken
        })

    def apiRec(self, params):
        return self.__myGet(self.api, params)

    def __myGet(self, api, params):
        try:
            get = S.get(url=api, params=params, timeout=30)
            if get.status_code == 200:
                return get.json()
            elif get.status_code == 429:
                c = 1
                while c < 5 and get.status_code == 429:
                    time.sleep(3 * c)
                    print('Sleeping {} second'.format(3 * c))
                    get = S.get(url=self.api, params=params, timeout=30)
                    c += 1
                if get.status_code == 200:
                    return get.json()
            else:
                return {}
        except Exception as e:
            print('skipping', api, params)
            return {}

    def getQuery(self, params, l, listS):
        params.update({"action": "query",
                       "format": "json",
                       "redirects": 1})
        query = []

        data = self.__myGet(self.api, params)
        if isinstance(data['query'][l], list):
            query += data['query'][l]
        else:
            query.append(data['query'][l])

        while 'continue' in data:
            params[listS + 'continue'] = data['continue'][listS + 'continue']
            temp = self.__myGet(self.api, params)
            if len(temp) == 0:
                continue
            data = temp
            try:
                if isinstance(data['query'][l], list):
                    query += data['query'][l]
                else:
                    query.append(data['query'][l])
            except:
                print(data, temp)

        return query

    def getSubcatsRec(self, catName, rec=0):
        cats = []
        q = self.getQuery({
            "list": "categorymembers",
            "cmtitle": "Category:" + catName,
            "cmprop": "title",
            "cmtype": "subcat",
        }, 'categorymembers', 'cm')
        for cat in q:
            cats.append(cat['title'])
        if rec <= 0:
            return cats
        for subcat in cats:
            newCats = self.getSubcatsRec(subcat.split(':', 1)[1], rec=rec-1)
            for cat in newCats:
                if cat not in cats:
                    cats.append(cat)
        return cats

    def getPagesInCategory(self, catName, ns=0, rec=0):
        catName = catName.replace('_', ' ')
        pages = []
        cats = ['Category:' + catName]
        if rec >= 1:
            cats += self.getSubcatsRec(catName, rec=rec-1)
        for cat in cats:
            q = self.getQuery({
                "list": "categorymembers",
                "cmtitle": cat,
                "cmprop": "title",
                "cmnamespace": ns
            }, 'categorymembers', 'cm')
            for page in q:
                pages.append(Page(self, page['title'], page['ns']))
        return pages

    def matrixToWikitable(self, matrix):
        text = '{| class="wikitable sortable"\n'
        text += '!' + '!!'.join(matrix[0]) + '\n'
        for i in range(1, len(matrix)):
            if isinstance(matrix[i], list) and len(matrix[i]) == len(matrix[0]):
                row = (str(x) if x else ' ' for x in matrix[i])
                text += '|-\n|' + '||'.join(row) + '\n'
        text += '|}'
        return text



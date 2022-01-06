import pywikibot as pw
import time
from pywikibot import pagegenerators as pg

site = pw.Site('wikidata', 'wikidata')
repo = site.data_repository()

g = site.search(' փոետրվարի ')

for p in g:
    try:
        time.sleep(10)
        item = pw.ItemPage(repo, p.title())
        if 'hy' in item.get()['descriptions']:
            d = item.get()['descriptions']['hy']
            newD = d.replace('փոետրվարի', 'փետրվարի')
            item.editDescriptions(descriptions={'hy': newD}, summary='Fixing a typo, -փոետրվարի +փետրվարի')
    except:
        pass

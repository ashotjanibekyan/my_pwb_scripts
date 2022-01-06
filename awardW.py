import requests
import pywikibot as pw
from pywikibot import pagegenerators as pg

hash = {}

wikidata = pw.Site('wikidata', 'wikidata')
hywiki = pw.Site('hy', 'wikipedia')
enwiki = pw.Site('en', 'wikipedia')
cat = pw.Category(hywiki, "Կատեգորիա:Հոդվածներ, որոնք մրցանակակիրների կատեգորիայի կարիք ունեն")
catgen = pg.CategorizedPageGenerator(cat, recurse=False)
for page in catgen:
    item = pw.ItemPage.fromPage(page, lazy_load=True)
    if item.exists() and (not item.isRedirectPage()) and 'P166' in item.get()['claims']:
        awards = item.get()['claims']['P166']
        for award in awards:
            if not award.getTarget().isRedirectPage() and 'P2517' in award.getTarget().get()['claims']:
                try:
                    award.getTarget().get()['claims']['P2517'][0].getTarget().getSitelink(hywiki)
                except:
                    title = award.getTarget().get()['claims']['P2517'][0].getTarget().title()
                    if title in hash:
                        hash[title]+=1
                    else:
                        hash[title]=1
data = []
for q in hash:
    data.append((q, hash[q]))
data = sorted(data, key=lambda tup: tup[1], reverse=True)

c = 0
text = ''
for item in data:
    if item[1] == 1:
        break
    if c % 10 == 0:
        text += '== Մասնակից ' + str(int((c + 10)/10)) + ' ==\n'
    text += '#[[:d:' + item[0] + ']] - ' + str(item[1]) + '\n'
    c+=1

statPage = pw.Page(hywiki, 'Մասնակից:ԱշոտՏՆՂ/ցանկեր/պակասող մրցանակակիրների կատեգորիաներ')
statPage.text = text
statPage.save(summary='թարմացում')
        

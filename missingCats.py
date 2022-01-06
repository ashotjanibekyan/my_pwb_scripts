import pywikibot as pw
from pywikibot import pagegenerators as pg
import datetime
import os
import sys

missingCats = {}

enwiki = pw.Site('en', 'wikipedia')
hywiki = pw.Site('hy', 'wikipedia')

def isAdministrative(itemData):
    if 'P31' in itemData['claims']:
        for claim in itemData['claims']['P31']:
            if claim.getTarget().title() == 'Q15647814' or claim.getTarget().title() == 'Q24046192':
                return True
    return False

def safeFromPage(page):
    item = pw.ItemPage.fromPage(page, lazy_load=True)
    if not item.exists():
        return None
    while item.isRedirectPage():
        if not item.exists():
            return None
        item = item.getRedirectTarget()
    return item

def suggestCat(page):
    existingCats = {}

    gen = page.categories()
    for cat in gen:
        if cat.exists():
            catItem = safeFromPage(cat)
            if catItem:
                existingCats[catItem.title()] = True
    item = safeFromPage(page)
    if item:
        itemData = item.get()
        entitle = None
        if 'enwiki' in itemData['sitelinks']:
            entitle = itemData['sitelinks']['enwiki'].title
        else:
            return None

        enpage = pw.Page(enwiki, entitle)
        enCatGen = enpage.categories()
        for enCat in enCatGen:
            if not enCat.exists():
                continue
            if enCat.isHiddenCategory():
                continue
            enCatItem = safeFromPage(enCat)
            if enCatItem and not (enCatItem.title() in existingCats):
                enCatItemData = enCatItem.get()
                if isAdministrative(enCatItemData):
                    return None
                if enCatItem.title() in missingCats:
                    missingCats[enCatItem.title()][0] += 1
                else:
                    title = 'en:Category:' + enCatItemData['sitelinks']['enwiki'].title
                    if 'hywiki' in enCatItemData['sitelinks']:
                        title = 'Կատեգորիա:' + enCatItemData['sitelinks']['hywiki'].title
                    missingCats[enCatItem.title()] = [1, title]


def saveHash(hash, pageToSave):
    data = []
    for q in hash:
        data.append((hash[q][1], hash[q][0]))
    data = sorted(data, key=lambda tup: tup[1], reverse=True)

    c = 0
    text = ''
    for item in data:
        if item[1] == 1 or c > 9000:
            break
        if c % 30 == 0:
            text += '== Մասնակից ' + str(int((c + 30)/30)) + ' ==\n'
        text += '#[[:' + item[0] + ']] - ' + str(item[1]) + '\n'
        c+=1

    statPage = pw.Page(hywiki, pageToSave)
    statPage.text = text
    statPage.save(summary='թարմացում')

def main(args):
    if not len(args) == 4:
        print('abort')
        print(args)
        return
    cat = pw.Category(hywiki, args[1])
    catgen = pg.CategorizedPageGenerator(cat, recurse=int(args[3]))
    for page in catgen:
        suggestCat(page)
    saveHash(missingCats, args[2])

with open('check.txt', 'a', encoding='utf-8') as f:
    f.write('\n*' + str(sys.argv) + ' - ' + str(datetime.datetime.now()) + ' - ' + str(os.getpid()))

print(datetime.datetime.now())
main(sys.argv)
print(datetime.datetime.now())

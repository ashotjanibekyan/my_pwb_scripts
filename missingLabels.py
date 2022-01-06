import pywikibot as pw
import wikiscripts as ws

hywiki = ws.Wiki('hy', 'wikipedia')
wikidata = ws.Wiki('wikidata', 'wikidata')

def Qs_from_article(name):
    res = hywiki.getQuery({
        "action": "query",
        "format": "json",
        "prop": "wbentityusage",
        "titles": name,
        "formatversion": "2",
    }, "pages", "wbeu")
    Qs = []
    for r in res:
        for q in r['wbentityusage']:
            if q not in Qs:
                Qs.append(q)
    return Qs

def needs_hy_label(Q):
    res = wikidata.apiRec({
        "action": "wbgetentities",
        "format": "json",
        "ids": Q,
        "props": "labels",
        "languages": "hy|en|ru",
        "formatversion": "2"
    })
    if "success" in res and 'entities' in res and Q in res['entities'] and 'labels' in res['entities'][Q]:
        labels = res['entities'][Q]['labels']
        if 'hy' not in labels:
            return [ 
                labels['en']['value'] if 'en' in labels else '',
                labels['ru']['value'] if 'ru' in labels else ''
            ]
        else:
            return None

def main():
    cat1 = set(page.title for page in hywiki.getPagesInCategory("Վիքիպեդիա:Վիքիդատայի անգլերեն պիտակով տարրեր պարունակող էջեր"))
    cat2 = set(page.title for page in hywiki.getPagesInCategory("Վիքիպեդիա:Վիքիդատայի հայերեն չթարգմանված տարրեր պարունակող հոդվածներ"))
    articles = list(cat1.union(cat2))
    freq = {}
    for article in articles:
        Qs = Qs_from_article(article)
        for Q in Qs:
            if Q in freq:
                freq[Q]+=1
            else:
                freq[Q] =1
    unlabel_freq = {}
    unlabel_freq_cat = {}
    for Q in freq:
        if freq[Q] < 3:
            continue
        needs_hy = needs_hy_label(Q)
        if needs_hy:
            if 'Category:' in needs_hy[0] or 'Категория:' in needs_hy[1]:
                 unlabel_freq_cat[Q] = [freq[Q]] + needs_hy
            else:
                unlabel_freq[Q] = [freq[Q]] + needs_hy

    sorted_freq = sorted(unlabel_freq, key=unlabel_freq.get, reverse=True)
    res = [['Տարր', 'Օգտագործման քանակ', 'Անգլերեն պիտակ', 'Ռուսերեն պիտակ']]
    for Q in sorted_freq:
        if 'P' in Q:
            res.append( ['[[d:Property:' + Q + ']]'] + [str(i) for i in unlabel_freq[Q]] )
        else:
            res.append( ['[[d:' + Q + ']]'] + [str(i) for i in unlabel_freq[Q]] )
        
    sorted_freq_cat = sorted(unlabel_freq_cat, key=unlabel_freq_cat.get, reverse=True)

    res_cat = [['Տարր', 'Օգտագործման քանակ', 'Անգլերեն պիտակ', 'Ռուսերեն պիտակ']]
    for Q in sorted_freq_cat:
        if 'P' in Q:
            res_cat.append( ['[[d:Property:' + Q + ']]'] + [str(i) for i in unlabel_freq_cat[Q]] )
        else:
            res_cat.append( ['[[d:' + Q + ']]'] + [str(i) for i in unlabel_freq_cat[Q]] )
    return res, res_cat

matrix, matrix_cat = main()

page = pw.Page(pw.Site('hy', 'wikipedia'), 'Մասնակից:ԱշոտՏՆՂ/ցանկեր/շատ_օգտագործվող_չթարգմանված_տարրեր')
page.text = 'Տարրերը թարգմանելու համար կարող եք օգտվել [https://hylabels.toolforge.org/ Hylabels] գործիքից։\n* [[Մասնակից:ԱշոտՏՆՂ/ցանկեր/շատ_օգտագործվող_չթարգմանված_տարրեր/կատեգորիա]]\n' + hywiki.matrixToWikitable(matrix)
page.save(summary='թարմացում', botflag=False)

page = pw.Page(pw.Site('hy', 'wikipedia'), 'Մասնակից:ԱշոտՏՆՂ/ցանկեր/շատ_օգտագործվող_չթարգմանված_տարրեր/կատեգորիա')
page.text = 'Հայերեն Վիքիպեդիայում պետք է ստեղծել այս կատեգորիաները։\n* [[Մասնակից:ԱշոտՏՆՂ/ցանկեր/շատ_օգտագործվող_չթարգմանված_տարրեր]]\n' + hywiki.matrixToWikitable(matrix_cat)
page.save(summary='թարմացում', botflag=False)

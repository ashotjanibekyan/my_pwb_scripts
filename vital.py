# -*- coding: utf-8 -*-
import pywikibot as pw
from wikiscripts import wikiscripts as ws
import re

def r(i):
    return round( i / 100.0 ) * 100

def missingArticles(_fromwiki, _towiki, category, skip_size, extra_lang):
    fromwiki = ws.Wiki(_fromwiki, 'wikipedia')
    towiki = ws.Wiki(_towiki, 'wikipedia')
    
    talkpages = fromwiki.getPagesInCategory(category, ns=1)
    text = '== [[:' + _fromwiki + ':Category:' + category + ']] == \n'
    if skip_size:
        if extra_lang:
            data = [ ['Անգլերեն հոդված', 'Ռուսերեն հոդված', 'Հայերեն հոդված', 'Անաղբյուր (hy)', 'մլ N'] ]
        else:
            data = [ ['Անգլերեն հոդված', 'Հայերեն հոդված', 'Անաղբյուր (hy)', 'մլ N'] ]
    else:
        data = [ ['Անգլերեն հոդված', 'en չափ', 'Հայերեն հոդված', 'hy չափ', 'Անաղբյուր (hy)', 'մլ N'] ]
    for talkpage in talkpages:
        namespace, sep, title = talkpage.title.partition(':')
        if title == talkpage.title:
            continue
        page = ws.Page(fromwiki, title)
        sitelinks = page.getSiteLinks()
        topage = sitelinks[towiki.lang + towiki.project] if sitelinks and towiki.lang + towiki.project in sitelinks else None
        totitle = None
        if topage:
            totitle = str(topage)
            totitle = totitle.replace('[[:hy:', '[[')
        extrapage = sitelinks[extra_lang + 'wikipedia'] if extra_lang and sitelinks and extra_lang + 'wikipedia' in sitelinks else None
        unsource = 'այո' if topage and 'Կատեգորիա:Անաղբյուր և լրացուցիչ աղբյուրների կարիք ունեցող հոդվածներ' in topage.categories() else ''
        iwN = len(sitelinks) if sitelinks else 1
        if skip_size:
            if extra_lang:
                data.append( [page, extrapage, totitle, unsource, iwN] )
            else:
                data.append( [page, totitle, unsource, iwN] )
        else:
            data.append( [page, r(page.size()), totitle, r(topage.size()) if topage else None, unsource, iwN] )
    return text + towiki.matrixToWikitable(data)


def run(fromwiki, towiki, cats, _savepage, skip_size=False, extra_lang=None):
    try:
        savepage = pw.Page(pw.Site(towiki, 'wikipedia'), _savepage)
        text = ''
        for cat in cats:
            text += '\n' + missingArticles(fromwiki, towiki, cat, skip_size=skip_size, extra_lang=extra_lang)
        savepage.text = text
        savepage.save(summary='թարմացում')
    except:
        pass

#run('en', 'hy', ['Top-importance Armenian articles', 'High-importance Armenian articles', 'Mid-importance Armenian articles', 'Low-importance Armenian articles'], 'Մասնակից:ԱշոտՏՆՂ/ցանկեր/կարևորագույն հոդվածներ/Հայաստան')

run('en', 'hy', ['Top-importance Linguistics articles',
                 'High-importance Linguistics articles',
                 'Mid-importance Linguistics articles'],
    'Մասնակից:ԱշոտՏՆՂ/ցանկեր/կարևորագույն հոդվածներ/լեզվաբանություն'
   )


run('en', 'hy', ['WikiProject Film core articles'], 'Մասնակից:ԱշոտՏՆՂ/ցանկեր/կարևորագույն հոդվածներ/ֆիլմեր')

run('en', 'hy', ['Top-importance medicine articles',
                 'High-importance medicine articles'],
    'Մասնակից:ԱշոտՏՆՂ/ցանկեր/կարևորագույն հոդվածներ/բժշկություն'
   )

run('en', 'hy', ['Top-Priority mathematics articles'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Անգլերեն Վիքիպեդիայից/կարևորագույն')
run('en', 'hy', ['High-Priority mathematics articles'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Անգլերեն Վիքիպեդիայից/բարձր կարևորության')
run('en', 'hy', ['Mid-Priority mathematics articles'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Անգլերեն Վիքիպեդիայից/միջին կարևորության')
run('en', 'hy', ['Low-Priority mathematics articles'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Անգլերեն Վիքիպեդիայից/ցածր կարևորության')
run('en', 'hy', ['FA-Class mathematics articles'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Անգլերեն Վիքիպեդիայից/ԸՀ կարգավիճակի')
run('en', 'hy', ['FL-Class mathematics articles'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Անգլերեն Վիքիպեդիայից/ԸՑ կարգավիճակի')
run('en', 'hy', ['A-Class mathematics articles'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Անգլերեն Վիքիպեդիայից/Ա կարգավիճակի')
run('en', 'hy', ['GA-Class mathematics articles'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Անգլերեն Վիքիպեդիայից/ԼՀ կարգավիճակի')
run('en', 'hy', ['B-Class mathematics articles'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Անգլերեն Վիքիպեդիայից/Բ կարգավիճակի')
run('en', 'hy', ['C-Class mathematics articles'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Անգլերեն Վիքիպեդիայից/Գ կարգավիճակի')
run('en', 'hy', ['List-Class mathematics articles'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Անգլերեն Վիքիպեդիայից/ցանկ կարգավիճակի')
run('ru', 'hy', ['Статьи проекта Математика высшей важности'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Ռուսերեն Վիքիպեդիայից/կարևորագույն')
run('ru', 'hy', ['Статьи проекта Математика высокой важности'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Ռուսերեն Վիքիպեդիայից/բարձր կարևորության')
run('ru', 'hy', ['Статьи проекта Математика средней важности'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Ռուսերեն Վիքիպեդիայից/միջին կարևորության')
run('ru', 'hy', ['Статьи проекта Математика низкой важности'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Ռուսերեն Վիքիպեդիայից/ցածր կարևորության')
run('ru', 'hy', ['Избранные статьи проекта Математика'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Ռուսերեն Վիքիպեդիայից/ԸՀ կարգավիճակի')
run('ru', 'hy', ['Избранные списки проекта Математика'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Ռուսերեն Վիքիպեդիայից/ԸՑ կարգավիճակի')
run('ru', 'hy', ['Добротные статьи проекта Математика'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Ռուսերեն Վիքիպեդիայից/Ա կարգավիճակի')
run('ru', 'hy', ['Хорошие статьи проекта Математика'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Ռուսերեն Վիքիպեդիայից/ԼՀ կարգավիճակի')
run('ru', 'hy', ['Статьи проекта Математика I уровня'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Ռուսերեն Վիքիպեդիայից/Բ կարգավիճակի')
run('ru', 'hy', ['Статьи проекта Математика II уровня'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Ռուսերեն Վիքիպեդիայից/Գ կարգավիճակի')
run('ru', 'hy', ['Списки проекта Математика'], 'Վիքինախագիծ:Մաթեմատիկա/Հոդվածներ Ռուսերեն Վիքիպեդիայից/ցանկ կարգավիճակի')

run('en', 'hy', ['Top-importance physics articles',
                 'High-importance physics articles'],
    'Մասնակից:ԱշոտՏՆՂ/ցանկեր/կարևորագույն հոդվածներ/ֆիզիկա'
   )

run('en', 'hy', ['Top-importance Turkey articles',
                 'High-importance Turkey articles',
                 'Mid-importance Turkey articles'],
    'Մասնակից:Armenmir/Turkey', skip_size=True, extra_lang='ru'
   )

run('en', 'hy', ['Top-importance Greek articles',
                 'High-importance Greek articles',
                 'Mid-importance Greek articles'],
    'Մասնակից:ԱշոտՏՆՂ/ցանկեր/Հունաստան', extra_lang='ru', skip_size=True
   )


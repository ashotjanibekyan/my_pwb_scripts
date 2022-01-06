import toolforge
import pywikibot as pw
import sys

def catCompleter(sourcelang, sourcecat, homelang, homecat):
    homewiki = pw.Site(homelang, 'wikipedia')
    homeconn = toolforge.connect(homelang + 'wiki')
    sourceconn = toolforge.connect(sourcelang + 'wiki')

    homequery = '''SELECT ll_title, page_title FROM categorylinks INNER JOIN langlinks ON cl_from = ll_from
AND ll_lang = \'''' + sourcelang + '''\' INNER JOIN page ON page_id = ll_from WHERE cl_to =\'''' + homecat + '''\' AND page_namespace=0'''

    sourcequery = '''SELECT ll_title, page_title FROM categorylinks INNER JOIN langlinks ON cl_from = ll_from
AND ll_lang = \'''' + homelang + '''\' INNER JOIN page ON page_id = ll_from WHERE cl_to =\'''' + sourcecat + '''\' AND page_namespace=0'''

    homepages = {}
    with homeconn.cursor() as cur:
        cur.execute(homequery)
        print(homequery)
        results = cur.fetchall()
        for r in results:
            homepages[r[1].decode('utf-8').replace('_', ' ')] = True
    with sourceconn.cursor() as cur:
        cur.execute(sourcequery)
        print(sourcequery)
        results = cur.fetchall()
        for r in results:
            if r[0].decode('utf-8') not in homepages:
                page = pw.Page(homewiki, r[0].decode('utf-8'))
                if page.exists():
                    cats = pw.textlib.getCategoryLinks(page.text, homewiki)
                    cats.append(homecat)
                    page.text = pw.textlib.replaceCategoryLinks(page.text, cats, site=homewiki)
                    page.save(summary='+[[Category:' + homecat + ']]` ըստ [[:' + sourcelang + ':Category:' + sourcecat + ']]-ի')
                else:
                    print(page)

catCompleter(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

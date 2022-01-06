import toolforge, re, time
import pywikibot as pw
from scripts.userscripts import wikiscripts as ws

hywiki = pw.Site('hy', 'wikipedia')
ws_hywiki = ws.Wiki('hy', 'wikipedia')

query = '''SELECT DISTINCT page_title, 
                cl_to 
FROM   categorylinks 
       JOIN page 
         ON page_id = cl_from 
WHERE  page_namespace = 2 
       AND cl_to NOT IN (SELECT page_title 
                         FROM   page 
                                JOIN page_props 
                                  ON page_id = pp_page 
                         WHERE  pp_propname = 'hiddencat') 
       AND cl_to IN (SELECT cl_to 
                     FROM   categorylinks 
                            JOIN page 
                              ON page_id = cl_from 
                     WHERE  page_namespace = 0);'''

conn = toolforge.connect('hywiki')

skip = {}
skipPage = pw.Page(hywiki, 'Մասնակից:ԱշոտՏՆՂ/ցանկեր/հոդվածների հետ նույն կատեգորիայում ապրող մասնակցային էջեր/անտեսել')
if skipPage.exists():
    skipPages = skipPage.text.splitlines()
    for line in skipPages:
        line = re.sub(r'^\* *(.+) *\n?', r'\1', line)
        line = line.replace('Մասնակից:', '')
        line = line.replace(' ', '_')
        skip[line] = True

with conn.cursor() as cur:
    cur.execute(query)
    results = cur.fetchall()
    text = [['Մասնակցային էջ', 'Կատեգորիա']]
    for r in results:
        if r[0].decode('utf-8') not in skip:
            thispage = pw.Page(hywiki, 'Մասնակից:' + r[0].decode('utf-8'))
            thispage.text = re.sub(r'\[\[([Կկ]ատեգորիա|[Cc]ategory):', '[[:Կատեգորիա:', thispage.text)
            thispage.save(summary='Կատեգորիան հեռացնում եմ ավազարկղից')
            time.sleep(30)
            if list(filter(lambda x : not x.isHiddenCategory(), list(thispage.categories()))):
                text.append(['[[Մասնակից:' + r[0].decode('utf-8') + ']]', '[[:Կատեգորիա:' + r[1].decode('utf-8') + ']]'])
    p = pw.Page(hywiki, 'Մասնակից:ԱշոտՏՆՂ/ցանկեր/հոդվածների հետ նույն կատեգորիայում ապրող մասնակցային էջեր')
    p.text = ws_hywiki.matrixToWikitable(text)
    p.save(summary='թարմացում', botflag=False)

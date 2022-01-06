import toolforge
from wikiscripts import wikiscripts as ws
import pywikibot as pw

hywiki = ws.Wiki('hy', 'wikipedia')
ruwiki = ws.Wiki('ru', 'wikipedia')
enwiki = ws.Wiki('en', 'wikipedia')

query = '''SELECT
  page_title, page_len
FROM page
WHERE page_namespace = 0
AND page_is_redirect = 0
AND page_id NOT IN (SELECT
                      tl_from
                    FROM templatelinks
                    WHERE (tl_title = 'Բազմիմաստություն' or
                           tl_title = 'Տարվա_նավարկում' or
                           tl_title = 'Մեծ_Հայքի_վարչական_բաժանում' or
                           tl_title = 'Գիրք:ՀՀՖՕՀՏԲ')
                    AND tl_namespace = 10)
and page_id not in (select cl_from
                    from categorylinks
                    where cl_to = 'Նյութեր_տեղանունների_բառարանից' or
                                  cl_to = 'Ազգանուններ_այբբենական_կարգով')
ORDER BY page_len ASC
LIMIT 10000;'''

en = '{| class="wikitable sortable"\n!Հայերեն հոդված!!hy չափ!!Անգլերեն հոդված!!en չափ\n'
ru = '{| class="wikitable sortable"\n!Հայերեն հոդված!!hy չափ!!Ռուսերեն հոդված!!ru չափ\n'
total = 'Ցակից հեռացվել են «Նյութեր տեղանունների բառարանից» և «Ազգանուններ այբբենական կարգով» կատեգորիաների հոդվածները։ Նաև Բազմիմաստություն, Տարվա նավարկում, և Գիրք:ՀՀՖՕՀՏԲ կաղապարն ունեցող հոդվածները։\n'
total+= '{| class="wikitable sortable"\n!Հոդված!!Չափ\n'


conn = toolforge.connect('hywiki')
with conn.cursor() as cur:
    cur.execute(query)
    results = cur.fetchall()
    for r in results:
        total+='|-\n|[[' + str(r[0].decode('utf-8')) + ']]||' + str(r[1]) + '\n'
        hypage = ws.Page(hywiki, r[0].decode('utf-8'))
        enpage = hypage.convertTo(enwiki)
        if enpage and '<ref' in enpage.read() and enpage.size() > hypage.size():
            en+='|-\n|' + str(hypage) + '||' + str(r[1]) + '||' + str(enpage) + '||' + str(enpage.size()) + '\n'
        
        rupage = hypage.convertTo(ruwiki)
        if rupage and '<ref' in rupage.read() and rupage.size() > hypage.size():
            ru+='|-\n|' + str(hypage) + '||' + str(r[1]) + '||' + str(rupage) + '||' + str(rupage.size()) + '\n'

en+='|}'
ru+='|}'
total+='|}'


hywiki_p = pw.Site('hy', 'wikipedia')

totalsubpage = pw.Page(hywiki_p, 'Մասնակից:ԱշոտՏՆՂ/ցանկեր/շատ կարճ հոդվածներ')
totalsubpage.text = total
totalsubpage.save(summary='թարմացում')
ensubpage = pw.Page(hywiki_p, 'Մասնակից:ԱշոտՏՆՂ/ցանկեր/շատ կարճ հոդվածներ/en')
ensubpage.text = en
ensubpage.save(summary='թարմացում')
rusubpage = pw.Page(hywiki_p, 'Մասնակից:ԱշոտՏՆՂ/ցանկեր/շատ կարճ հոդվածներ/ru')
rusubpage.text = ru
rusubpage.save(summary='թարմացում')

import pymysql  # We will use pymysql to connect to the database
import os
import pywikibot as pw
import re

hywiki = pw.Site('hy', 'wikipedia')
host = os.environ['MYSQL_HOST']
user = os.environ['MYSQL_USERNAME']
password = os.environ['MYSQL_PASSWORD']
conn = pymysql.connect(
    host=host,
    user=user,
    password=password
)

with conn.cursor() as cur:
    cur.execute('use hywiki_p')
    cur.execute("""
        SELECT page_title,
               page_len
        FROM   page
        WHERE  page_namespace = 0
               AND page_len > 3010
               AND page_id IN (SELECT cl_from 
                               FROM   categorylinks
                               WHERE cl_to = 'Անավարտ_հոդվածներ'
                              )
    """)
    results = cur.fetchall()
    print(len(results))
    for r in results:
        page = pw.Page(hywiki, r[0].decode('utf-8'))
        text = page.text
        page.text = re.sub(r'\{\{([Bb]io\-stub|[Աա]նձ\-անավարտ|[Աա]նավարտ\-աստղագիտություն|[Եե]րգիչ-անավարտ|[Կկ]ենսագրություն\-անավարտ|[Աա]նավարտ)\}\}', '', text)
        print('\n')
        if len(page.text.encode('utf-8')) >= 3000 and page.text != text:
            page.save(summary='հեռացնում եմ անավարտի պիտակը, քանի որ հոդվածը ունի ' + str(len(page.text.encode('utf-8'))) + ' բայթ ծավալ')
        elif page.text == text:
            print(page.text[int(len(page.text)) - 300:])

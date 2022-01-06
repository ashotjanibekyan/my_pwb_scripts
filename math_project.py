import pywikibot as pw
from pywikibot import pagegenerators as pg
import re
from scripts.userscripts import wikiscripts as ws
import pywikibot.data.api as api
hywiki = pw.Site('hy', 'wikipedia')
enwiki = pw.Site('en', 'wikipedia')

hywiki_ws = ws.Wiki('hy', 'wikipedia')
enwiki_ws = ws.Wiki('en', 'wikipedia')
'''
temp = pw.Page(enwiki, 'Template:Maths rating')
gen = temp.getReferences(only_template_inclusion=True, namespaces=1, follow_redirects=False)

fields = {
    'algebra' : 'հանրահաշիվ',
    'analysis' : 'անալիզ',
    'applied' : 'կիրառական',
    'applied mathematics' : 'կիրառական',
    'basics' : 'տարրական',
    'discrete' : 'դիսկրետ',
    'discrete mathematics' : 'դիսկրետ',
    'foundations' : 'հիմքեր',
    'foundations, logic, and set theory' : 'հիմքեր, տրամաբանություն և բազմությունների տեսություն',
    'logic' : 'բազմությունների տեսություն',
    'set theory' : 'տրամաբանություն',
    'general' : 'ընդհանուր',
    'geometry' : 'երկրաչափություն',
    'history' : 'պատմություն',
    'mathematical physics' : 'ֆիզիկա',
    'mathematician' : 'մաթեմատիկոս',
    'mathematicians' : 'մաթեմատիկոս',
    'number theory' : 'թվերի տեսություն',
    'probability' : 'հավանականություն',
    'probability and statistics' : 'հավանականություն և վիճակագրություն',
    'statistics' : 'վիճակագրություն',
    'topology' : 'տոպոլոգիա'
}

priorities = {
    'top' : 'բարձրագույն',
    'high' : 'բարձր',
    'mid' : 'միջին',
    'low' : 'ցածր'
}

def create_hy_template(text):
    templates = r'(Maths rating|Math rating|Maths rating small|Mathrating|WikiProject Maths|WikiProject Math|WP Maths|WPMath|WikiProject Mathematics rating|WPMATHEMATICS)'
    m = re.search(r'(\{\{' + templates + r'[^}]+\}\})', text, re.IGNORECASE)
    if m:
        template = m.group(0).replace('\n', '')
        
        priority_reg = r'\{\{' + templates + r'.*\| *priority *= *([^|}]+).*\}\}'
        priority = re.sub(priority_reg, r'\2', template, flags=re.IGNORECASE)
        if priority == template:
            priority = ''
            
        field_reg = r'\{\{' + templates + r'.*\| *field *= *([^|}]+).*\}\}'
        field = re.sub(field_reg, r'\2', template, flags=re.IGNORECASE)
        if field == template:
            field = ''
            
        vital_reg = r'\{\{' + templates + r'.*\| *vital *= *([^|}]+).*\}\}'
        vital = re.sub(vital_reg, r'\2', template, flags=re.IGNORECASE)
        if vital == template:
            vital = ''
            
        importance_reg = r'\{\{' + templates + r'.*\| *importance *= *([^|}]+).*\}\}'
        importance = re.sub(importance_reg, r'\2', template, flags=re.IGNORECASE)
        if importance == template:
            importance = ''
        
        fieldhy = ''
        if field.lower().strip() in fields:
            fieldhy = ' | բնագավառ = ' + fields[field.lower().strip()]
        
        
        priorityhy = ''
        if importance.lower().strip() in priorities:
            priorityhy = ' | կարևորություն = ' + priorities[importance.lower().strip()]
            
        if priority.lower().strip() in priorities:
            priorityhy = ' | կարևորություն = ' + priorities[priority.lower().strip()]
        
        vitalhy = ''
        if vital:
            vitalhy = ' | կարևորագույն = ' + 'այո'
        
        hytemplate = '{{Վիքինախագիծ Մաթեմատիկա' + fieldhy + priorityhy + vitalhy + '}}'
        return hytemplate
    return None

for p in gen:
    skiped = False
    ws_en_page = ws.Page(enwiki_ws, p.title(with_ns=False))
    try:
        ws_hy_page = ws_en_page.convertTo(hywiki_ws)
    except:
        continue
    if ws_hy_page:
        hytemplate = create_hy_template(p.text)
        if not hytemplate:
            skiped = True
            continue
        hy_page_talk = pw.Page(hywiki, ws_hy_page.title).toggleTalkPage()
        hy_page_talk.text = re.sub(r'\{\{Վիքինախագիծ Մաթեմատիկա\}\}\n?', '', hy_page_talk.text)
        if '{{Վիքինախագիծ Մաթեմատիկա' not in hy_page_talk.text:
            hy_page_talk.text = hytemplate + '\n' + hy_page_talk.text
            hy_page_talk.save(summary='+' + hytemplate + ', ըստ [[Special:PermaLink/7367323#{{Վիքինախագիծ_Մաթեմատիկա}}_կաղապարը_քննարկման_էջերում]]')
        else:
            skiped = True

'''

# views
def getViews(page):
    s = 0
    try:
        req = api.Request(site=hywiki, parameters={'action': 'query',
                                        'titles': page,
                                        'prop': 'pageviews'})
        pageviews = req.submit()['query']['pages'][str(page.pageid)]['pageviews']
        for day in pageviews:
            if pageviews[day]:
                s+=pageviews[day]
    except Exception as e:
        print(e)
        pass
    return s

cat = pw.Category(hywiki, 'Կատեգորիա:Մաթեմատիկական հոդվածներ')
data = []
for talkpage in cat.members():
    page = talkpage.toggleTalkPage()
    views = getViews(page)
    data.append([page, views])

data = [['Հոդված', 'Դիտումներ (վերջին 60 օրվա ընթացքում)']] + sorted(data[1:], key= lambda x : x[1], reverse=True)
viewpage = pw.Page(hywiki, 'Վիքինախագիծ:Մաթեմատիկա/Հաճախ դիտվող')
viewpage.text = ws.Wiki.matrixToWikitable(None, data[:501]).replace('[[hy:', '[[')
viewpage.save(summary='թարմացում')

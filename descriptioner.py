import pywikibot as pw
from pywikibot import pagegenerators as pg
import sys, datetime

site = pw.Site('wikidata', 'wikidata')

def run(from_lang, from_desc, to_lang, to_desc, site):
    q = '''SELECT ?item WHERE {{
      ?item schema:description "{}"@{}.
      FILTER(NOT EXISTS {{
        ?item schema:description ?itemdesc.
        FILTER(LANG(?itemdesc) = "{}")
      }})
    }}'''.format(from_desc, from_lang, to_lang)
    try:    
        gen = pg.WikidataSPARQLPageGenerator(q, site)
    except:
        gen = []
    for item in gen:
        try:
            item.editDescriptions({to_lang : to_desc}, summary='+{}:{} description based on {}:{}'.format(to_lang, to_desc, from_lang, from_desc))
        except Exception as e:
            print(e)

def scientific_articles():
    months = {
        'January' : 'հունվար',
        'February' : 'փետրվար',
        'March' : 'մարտ',
        'April' : 'ապրիլ',
        'May' : 'մայիս',
        'June' : 'հունիս',
        'July' : 'հուլիս',
        'August' : 'օգոստոս',
        'September' : 'սեպտեմբեր',
        'October' : 'հոկտեմբեր',
        'November' : 'նոյեմբեր',
        'December' : 'դեկտեմբեր'
    }
    for year in range(1900, datetime.datetime.now().year+1):
        for month in months:
            for day in range(1, 13):
                opt_1_en = 'scientific article published on {} {} {}'.format(str(day), month, str(year))
                opt_1_hy = '{} թվականի {}ի {}-ին հրատարակված գիտական հոդված'.format(str(year), months[month], str(day))
                run('en', opt_1_en, 'hy', opt_1_hy, site)

                opt_2_en = 'scientific article published on 0{} {} {}'.format(str(day), month, str(year))
                opt_2_hy = '{} թվականի {}ի {}-ին հրատարակված գիտական հոդված'.format(str(year), months[month], str(day))
                run('en', opt_2_en, 'hy', opt_2_hy, site)

                opt_3_en = 'scientific article published on {} {}'.format( month, str(year))
                opt_3_hy = '{} թվականի {}ին հրատարակված գիտական հոդված'.format(str(year), months[month])
                run('en', opt_3_en, 'hy', opt_3_hy, site)

def by_ref(s_q, from_desc, to_desc):
    def should_add(q):
        r = requests.get('https://www.wikidata.org/w/api.php?action=wbgetentities&ids=' + q + '&props=descriptions&languages=en|hy&format=json')
        j = r.json()
        if j['success'] and 'descriptions' in j['entities'][q]:
            desc = j['entities'][q]['descriptions']
            if 'en' in desc and desc['en']['value'] == from_desc and 'hy' not in desc:
                return True
        return False
    
    page = pw.ItemPage(site, s_q)
    gen = page.getReferences(follow_redirects=True)
    for i in gen:
        try:
            if re.match(r'^Q\d+$', i.title()) and should_add(i.title()):
                item = pw.ItemPage(site, i.title())
                item.editDescriptions({'hy' : to_desc}, summary='+hy:{} description based on en:{}'.format(to_desc, from_desc))
        except:
            continue

if len(sys.argv) == 5:
    from_lang, from_desc, to_lang, to_desc = sys.argv[-4:]
    run(from_lang, from_desc, to_lang, to_desc, site)

run('en', 'date in Gregorian calendar', 'hy', 'Գրիգորյան օրացույցի ամսաթիվ', site)
run('en', 'mountain in Australia', 'hy', 'լեռ Ավստրալիայում', site)
run('en', 'mountain in Indonesia', 'hy', 'լեռ Ինդոնեզիայում', site)
run('en', 'river in Brazil', 'hy', 'գետ Բրազիլիայում', site)
run('en', 'American politician', 'hy', 'ամերիկացի քաղաքական գործիչ', site)
run('en', 'actor', 'hy', 'դերասան', site)
run('en', 'human settlement in Myanmar', 'hy', 'բնակավայր Մյանմարում', site)
run('en', 'river in the United States of America', 'hy', 'գետ ԱՄՆ֊ում', site)
run('en', 'mountain in Iran', 'hy', 'լեռ Իրանում', site)
run('en', 'organization', 'hy', 'կազմակերպություն', site)
run('en', 'river in Indonesia', 'hy', 'գետ Ինդոնեզիայում', site)
run('en', 'French politician', 'hy', 'ֆրանսիացի քաղաքական գործիչ', site)
run('en', 'association football player', 'hy', 'ֆուտբոլիստ', site)
run('en', 'human settlement in India', 'hy', 'բնակավայր Հնդկաստանում', site)
run('en', 'human settlement in Italy', 'hy', 'բնակավայր Իտալիայում', site)
run('en', 'human settlement in Germany', 'hy', 'բնակավայր Գերմանիայում', site)
run('en', 'Unicode character', 'hy', 'Յունիկոդի նիշ', site)
run('en', 'encyclopedia article', 'hy', 'հանրագիտարանային հոդված', site)
run('en', 'Bank in India', 'hy', 'բանկ Հնդկաստանում', site)
run('en', 'asteroid', 'hy', 'աստերոիդ', site)
scientific_articles()
by_ref('Q318', 'galaxy', 'գալակտիկա')
by_ref('Q3863', 'asteroid', 'աստերոիդ')
by_ref('Q11173', 'chemical compound', 'քիմիական միացություն')
by_ref('Q101352', 'family name', 'ազգանուն')


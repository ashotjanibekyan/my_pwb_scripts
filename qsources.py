import pywikibot as pw
from pywikibot import pagegenerators
from datetime import date
from dateutil.relativedelta import relativedelta
import re
two_days = date.today() + relativedelta(days=-2)
one_days = date.today() + relativedelta(days=-1)
pwhywiki = pw.Site('hy', 'wikipedia')
newpages = list(pwhywiki.newpages(total=0,
                             end=str(two_days) + 'T00:00:00.000Z',
                             start=str(one_days) + 'T00:00:00.000Z',
                             namespaces=0))
for newpage in newpages:
    if newpage[0].exists() and newpage[0].toggleTalkPage().exists() and '<ref' in  newpage[0].text:
        if '{{ԹՀ' in newpage[0].toggleTalkPage().text:
            categories = [i.title() for i in newpage[0].categories()]
            m = list(set(re.findall(r'\{\{ԹՀ\|([^|]+)\|([^}|]+)', newpage[0].toggleTalkPage().text)))
            if m and 'Կատեգորիա:Բնօրինակում անաղբյուր հոդվածներ' not in categories:
                has_source = False
                for lang in m:
                    source_wiki = pw.Site(lang[0], 'wikipedia')
                    source_page = pw.Page(source_wiki, lang[1])
                    if '<ref' in source_page.text:
                        has_source = True
                        break
                if not has_source:
                    newpage[0].text = newpage[0].text + '\n[[Կատեգորիա:Բնօրինակում անաղբյուր հոդվածներ]]'
                    newpage[0].save(summary='+[[Կատեգորիա:Բնօրինակում անաղբյուր հոդվածներ]]')

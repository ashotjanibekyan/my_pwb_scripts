import requests
from bs4 import BeautifulSoup
import pywikibot as pw

url = 'https://www.worldometers.info/coronavirus/'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
total_cases = soup.find_all(class_='maincounter-number')[0].text.strip()
recovery_cases = soup.find_all(class_='maincounter-number')[2].text.strip()
death_cases = soup.find_all(class_='maincounter-number')[1].text.strip()
text = '''<div style="margin-top: 3px; margin-bottom: 4px; margin-left: 1px; margin-right: 1px; padding-top: 5px; padding-bottom: 5px; text-align:center; border-style: solid; background:#fafcfe; border:1px solid #a3b0bf;">\'''[[COVID-19 համավարակ]]\'''<br/><div style="font-size:85%;">{{{{hlist
|[[COVID-19 (կորոնավիրուսային վարակ 2019)|COVID-19 վարակ]]
|[[SARS-CoV-2 (կորոնավիրուս)|SARS-CoV-2 կորոնավիրուս]]
| Աշխարհում՝ {} վարակված

| {} բուժված

| {} մահ

}}}}</div></div>
'''.format(total_cases, recovery_cases, death_cases)
page = pw.Page(pw.Site('hy', 'wikipedia'), 'Կաղապար:ԸԻ/Հատուկ')
page.text = text
page.save('թարմացում ըստ https://www.worldometers.info/coronavirus/ կայքի')

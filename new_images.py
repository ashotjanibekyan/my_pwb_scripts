import pywikibot as pw
import requests, os, time, datetime, re, sys
from io import BytesIO
from PIL import Image
from pywikibot import pagegenerators as pg
from scripts.userscripts import toolforge

S = requests.Session()
URL = "https://hy.wikipedia.org/w/api.php"

def get_csrf_token():
    PARAMS_0 = {
        'action':"query",
        'meta':"tokens",
        'type':"login",
        'format':"json"
    }
    R = S.get(url=URL, params=PARAMS_0)
    DATA = R.json()
    LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

    PARAMS_1 = {
        'action':"login",
        'lgname':"ԱշբոտՏՆՂ",
        'lgpassword':"TeokratakanAratta28dbc",
        'lgtoken':LOGIN_TOKEN,
        'format':"json"
    }
    R = S.post(URL, data=PARAMS_1)
    PARAMS_2 = {
        'action':"query",
        'meta':"tokens",
        'format':"json"
    }
    R = S.get(url=URL, params=PARAMS_2)
    DATA = R.json()

    CSRF_TOKEN = DATA['query']['tokens']['csrftoken']
    return CSRF_TOKEN

def get_revs_to_del(image_name):
    get_old_rev = {'action':'query',
        'prop':'imageinfo',
        'titles': image_name,
        'iiprop':'archivename',
        'iilimit':'max',
        'formatversion':'2',
        'format': 'json'
    }
    r = requests.get(URL, get_old_rev)
    data = r.json()['query']['pages'][0]['imageinfo'][1:]
    result = []
    for i in data:
        if 'archivename' in i:
            result.append(i['archivename'])
    return result

def delete_old_revs(image_name):
    old_revs = get_revs_to_del(image_name)
    for old_rev in old_revs:
        version = re.sub(r'([^!]*)!.*', r'\1', old_rev)
        title = re.sub(r'[^!]*!(.*)', r'\1', old_rev)
        print(title)
        delete_old_rev = {
            'action': "revisiondelete",
            'target': 'Պատկեր:' + title,
            'type':'oldimage',
            'hide':'content',
            'ids':version,
            'reason':'Չօգտագործվող նիշք',
            'token':get_csrf_token(),
            'format':"json"
        }

        R = S.post(URL, data=delete_old_rev)


site = pw.Site('hy', 'wikipedia')

def is_large(file):
    return max(file.latest_file_info.width, file.latest_file_info.height) > 600
    

def resize_and_upload(file):
    if file.exists() and is_large(file):
        url = file.get_file_url()
        response = requests.get(url)
        try:
            img = Image.open(BytesIO(response.content))
        except OSError as e:
            print(e)
            return
        if max(img.height, img.width) <= 600:
            return
        ratio = 600 / max(img.height, img.width)
        h = int(img.height * ratio)
        w = int(img.width * ratio)
        img = img.resize((w, h), Image.ANTIALIAS)
        img.save(file.title())
        file.upload(file.title(), comment='կանոնակարգին համապատասխանող փոքր տարբերակ', ignore_warnings=True)
        os.remove(file.title())
        delete_old_revs(file.title())

conn = toolforge.connect('hywiki')
query = "select img_name, img_width, img_height from image where img_width > 600 or img_height > 600"
with conn.cursor() as cur:
    cur.execute(query)
    results = cur.fetchall()
    for r in results:
        file = pw.FilePage(site, r[0].decode('utf-8'))
        resize_and_upload(file)

temp1 = datetime.datetime.now()
temp2 = datetime.datetime.now()

while True:
    temp1 = datetime.datetime.now()
    gen = list(pg.LogeventsPageGenerator(site=site, logtype='upload', end=temp2 - datetime.timedelta(seconds=10)))
    for file in gen:
        try:
            resize_and_upload(file)
        except KeyboardInterrupt:
            sys.exit()
            pass
        except Exception as e:
            print(e)
    temp2 = temp1
    time.sleep(60 * 5)

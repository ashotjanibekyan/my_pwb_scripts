# -*- coding: utf-8 -*-

import requests
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
from time import sleep

endpoint_url = "https://query.wikidata.org/sparql"

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def prepare_session(S, URL):

    # Step 1: GET request to fetch login token
    PARAMS_0 = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS_0)
    DATA = R.json()

    LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

    # Step 2: POST request to log in. Use of main account for login is not
    # supported. Obtain credentials via Special:BotPasswords
    # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
    PARAMS_1 = {
        "action": "login",
        "lgname": "ԱշբոտՏՆՂ",
        "lgpassword": "TeokratakanAratta28dbc",
        "lgtoken": LOGIN_TOKEN,
        "format": "json"
    }

    R = S.post(URL, data=PARAMS_1)

    # Step 3: GET request to fetch CSRF token
    PARAMS_2 = {
        "action": "query",
        "meta": "tokens",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS_2)
    DATA = R.json()

    return DATA['query']['tokens']['csrftoken']


S = requests.Session()
URL = "https://www.wikidata.org/w/api.php"
CSRF_TOKEN = prepare_session(S, URL)

PARAMS_3 = {
    "action": "wbsetdescription",
    "format": "json",
    "id": "",
    "summary": '',
    "token": CSRF_TOKEN,
    "language": 'hy',
    "bot": 1,
    "value": ''
}
print('start')

ms = {
	'January': 'հունվարի',
	'February': 'փետրվարի',
	'March': 'մարտի',
	'April': 'ապրիլի',
	'May': 'մայիսի',
	'June': 'հունիսի',
	'July': 'հուլիսի',
	'August': 'օգոստոսի',
	'September': 'սեպտեմբերի',
	'October': 'հոկտեմբերի',
	'November': 'նոյեմբերի',
	'December': 'դեկտեմբերի'
}

for year in reversed(range(1900, 1941)):
    for m in ms:
        for d in range(1, 13):
            end = "scientific article published on {} {} {}".format(d, m, year)
            hyd = "{} թվականի {} {}-ին հրատարակված գիտական հոդված".format(year, ms[m], d)
            query = """
                SELECT ?item WHERE {{
                  ?item schema:description "{}"@en.
                  FILTER(NOT EXISTS {{
                    ?item schema:description ?itemdesc.
                    FILTER(LANG(?itemdesc) = "hy")
                  }})
                }}""".format(end)
            print(query)
            results = get_results(endpoint_url, query)
            print(len(results["results"]["bindings"]))
            for result in results["results"]["bindings"]:
                Q = result['item']['value'].replace('http://www.wikidata.org/entity/', '')
                PARAMS_3['id'] = Q
                PARAMS_3['value'] = hyd
                PARAMS_3['summary'] = 'based on en:' + end
                R = S.post(URL, data=PARAMS_3)
                sleep(10)
print('end')

import requests
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
from time import sleep

args = []
for arg in sys.argv:
    args.append(arg.replace('\\', ''))

endpoint_url = "https://query.wikidata.org/sparql"

print(args)

query = """SELECT ?item WHERE {{
  ?item schema:description "{}"@{}.
  FILTER(NOT EXISTS {{
    ?item schema:description ?itemdesc.
    FILTER(LANG(?itemdesc) = "{}") 
  }})
}}""".format(args[1], args[2], args[4])

print(query)

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)


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
    "summary": 'based on {}:{}'.format(args[2], args[1]),
    "token": CSRF_TOKEN,
    "language": args[4],
    "bot": 1,
    "value": args[3]
}
print('start')
for result in results["results"]["bindings"]:
    try:
        Q = result['item']['value'].replace('http://www.wikidata.org/entity/', '')
        PARAMS_3['id'] = Q
        R = S.post(URL, data=PARAMS_3)
#        print("{} is saved".format(Q))
#        print("Sleeping 15 sec")
        sleep(8)
    except not KeyboardInterrupt:
        continue
print('end')

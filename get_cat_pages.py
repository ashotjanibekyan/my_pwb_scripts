from scripts.userscripts import toolforge
import MySQLdb

conn = toolforge.connect('hywiki')


def pages_in_cat(cat_name, namespace):
    cat_name = cat_name.replace("'", "\\'")
    cat_name = cat_name.replace('"', '\\"')
    query = '''select page_title from page join categorylinks on page_id = cl_from where cl_to = '{}' and page_namespace = {}'''.format(cat_name, namespace)
    print(query)
    titles = []
    with conn.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()
        for r in results:
            titles.append(r[0].decode('utf-8'))
    return titles

PROCESSED_CATS = {}

def __get_all_categories(cat_name, rec):
    PROCESSED_CATS[cat_name] = True
    if rec < 0:
        return [cat_name]
    if rec == 0:
        return pages_in_cat(cat_name, 14)
    my_subcats = pages_in_cat(cat_name, 14) + [cat_name]
    result = my_subcats.copy()
    for cat in my_subcats:
        if cat in PROCESSED_CATS:
            continue
        result += __get_all_categories(cat, rec-1)
    return list(dict.fromkeys(result))


def get_all_categories(cat_name, rec):
    global PROCESSED_CATS
    PROCESSED_CATS = {}
    return __get_all_categories(cat_name, rec)

def articles_in_cat_rec(cat_name, rec=0):
    all_subcats = get_all_categories(cat_name, rec-1)
    articles = []
    for subcat in all_subcats:
        articles += pages_in_cat(subcat, 0)
    return list(dict.fromkeys(articles))

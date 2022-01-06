import toolforge
import pywikibot as pw
import sys

site = pw.Site('hy', 'wikipedia')
page = pw.Page(site, 'Մասնակից:ԱշոտՏՆՂ/Սևագրություն')

q1 = "select ips_site_page, ips_item_id from wb_items_per_site where ips_site_id = 'hywiki'"

q2 = "select replace(page_title, '_', ' '), page_namespace from page"

wikidataconn = toolforge.connect('wikidatawiki_p')
hywikiconn = toolforge.connect('hywiki_p')

text = ""
hywikitable = {}

nsMap = {0: "", 1: "Քննարկում", 2: "Մասնակից", 3: "Մասնակցի քննարկում", 4: "Վիքիպեդիա", 5: "Վիքիպեդիայի քննարկում", 6: "Պատկեր", 7: "Պատկերի քննարկում", 8: "MediaWiki", 9: "MediaWiki քննարկում", 10: "Կաղապար", 11: "Կաղապարի քննարկում", 12: "Օգնություն", 13: "Օգնության քննարկում", 14: "Կատեգորիա", 15: "Կատեգորիայի քննարկում", 100: "Պորտալ", 101: "Պորտալի քննարկում", 828: "Մոդուլ", 829: "Մոդուլի քննարկում", 2300: "Gadget", 2301: "Gadget talk", 2302: "Gadget definition", 2303: "Gadget definition talk", -2: "Մեդիա", -1: "Սպասարկող"}

with hywikiconn.cursor() as cur:
    cur.execute(q2)
    results = cur.fetchall()
    for r in results:
        ns = ''
        if not nsMap[r[1]] == '':
            ns = nsMap[r[1]] + ":"
        title = ns + r[0].decode('utf-8')
        hywikitable[title] = True

with wikidataconn.cursor() as cur:
    cur.execute(q1)
    results = cur.fetchall()
    for r in results:
        title = r[0].decode('utf-8')
        if title not in hywikitable:
            text+= '#[[:d:Q' + str(r[1]) + ']]\n'
page.text = text
page.save()

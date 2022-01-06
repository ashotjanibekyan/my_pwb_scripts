from wikiscripts import wikiscripts as ws
import get_cat_pages as cc
import pywikibot as pw
import sys, re

args = sys.argv  # cat source_wiki target_wiki cat_name save_to rec
TEXT = '''Այս էջում կարող եք գտնել «{}» կատեգորիայի հոդվածներում կատեգորիա ավելացնելու առաջարկներ։ Եթե կարծում եք, որ ինչ-որ \
հոդված չպետք է հայտնվի այս էջում,․ խնդրում ենք հոդվածի անունը ավելացնել [[{}]] էջում այնտեղ նշված ֆորմատով։ Եթե կարծում \
եք, որ ինչ-որ կատեգորիա չպետք է հայտնվի այս էջում, խնդրում ենք կատեգորիայի անունը ավելացնել [[{}]] էջում այնտեղ նշված \
ֆորմատով։\n'''.format(args[4].replace('_', ' '),
                     args[5].replace('_', ' ') + '/անտեսված հոդվածներ',
                     args[5].replace('_', ' ') + '/անտեսված կատեգորիաներ')


def list_to_freq(dic, l):
    for obj in l:
        if obj in dic:
            dic[obj] += 1
        else:
            dic[obj] = 1


def skip_page_to_dic(page):
    dic = {}
    if page.exists():
        lines = page.read().splitlines()
        for line in lines:
            if len(line) > 0 and line[0] == '*':
                line = re.sub(r'^\* *(.+) *\n?', r'\1', line)
                line = line.replace('_', ' ')
                dic[line] = True
    return dic


def find_freqs(target_wiki_articles, source_wiki, target_wiki, save_to_title):
    if len(target_wiki_articles) > 0 and isinstance(target_wiki_articles[0], str):
        target_wiki_articles = [ws.Page(target_wiki, i) for i in target_wiki_articles]
    source_wiki_cat_freq = {}
    target_wiki_cat_freq = {}
    skip_dic = skip_page_to_dic(ws.Page(target_wiki, save_to_title + '/անտեսված հոդվածներ'))

    for target_wiki_article in target_wiki_articles:
        if target_wiki_article.title in skip_dic:
            continue
        source_wiki_article = target_wiki_article.convertTo(source_wiki)
        if not source_wiki_article:
            continue
        target_wiki_article_cats = target_wiki_article.categories(hidden="!hidden")
        list_to_freq(target_wiki_cat_freq, target_wiki_article_cats)
        source_wiki_article_cats = source_wiki_article.categories(hidden="!hidden")
        list_to_freq(source_wiki_cat_freq, source_wiki_article_cats)
    return source_wiki_cat_freq, target_wiki_cat_freq


def process_raw_freqs(source_freq, target_freq, source_wiki, target_wiki, save_to_title):
    source_freq_converted = {}
    skip_dic = skip_page_to_dic(ws.Page(target_wiki, save_to_title + '/անտեսված կատեգորիաներ'))
    for cat_name in source_freq:
        if cat_name in skip_dic or source_freq[cat_name] < 3:
            continue
        cat = ws.Page(source_wiki, cat_name, ns=14)
        converted = cat.convertTo(target_wiki)
        if converted:
            if converted.title in target_freq:
                source_freq_converted[converted.title] = source_freq[cat_name] - target_freq[converted.title]
            else:
                source_freq_converted[converted.title] = source_freq[cat_name]
        else:
            source_freq_converted[cat_name] = source_freq[cat_name]
    sorted_freq = sorted(source_freq_converted, key=source_freq_converted.get, reverse=True)
    res = []
    for cat in sorted_freq:
        if source_freq_converted[cat] > 2:
            res.append((cat, source_freq_converted[cat]))
    return res


def make_suggestions_cat(cat_name, source_wiki, target_wiki, save_to_title, rec=0):
    """
        @type cat_name: str
        @type source_wiki: ws.Wiki
        @type target_wiki: ws.Wiki
        @type save_to: pw.Page
    """
    save_to = pw.Page(pw.Site(args[3], 'wikipedia'), save_to_title)
    target_wiki_articles = [ws.Page(target_wiki, title) for title in cc.articles_in_cat_rec(cat_name, rec=rec)]
    print(len(target_wiki_articles))
    raw_freqs = find_freqs(target_wiki_articles, source_wiki, target_wiki, save_to_title)
    raw_data = process_raw_freqs(raw_freqs[0], raw_freqs[1], source_wiki, target_wiki, save_to_title)
    text = '==' + cat_name + '==\n'
    for item in raw_data:
        if len(text.encode('utf-8')) > 100000:
            break
        if 'Category:' in item[0]:
            text += '\n# [[:en:' + item[0] + ']] - ' + str(item[1])
        elif 'Категория:' in item[0]:
            text += '\n# [[:ru:' + item[0] + ']] - ' + str(item[1])
        elif 'Կատեգորիա:' in item[0]:
            text += '\n# [[:' + item[0] + ']] - ' + str(item[1])
        else:
            text += '\n# ' + item[0] + ' - ' + str(item[1])
    save_to.text = TEXT + text
    save_to.save(summary='թարմացում', botflag=False)


if args[1] == 'cat':
    source_wiki = ws.Wiki(args[2], 'wikipedia')
    target_wiki = ws.Wiki(args[3], 'wikipedia')
    rec = int(args[6]) if len(args) == 7 else 0
    make_suggestions_cat(args[4], source_wiki, target_wiki, args[5], rec=rec)


#!/usr/bin/python
# -*- coding: utf-8 -*-

import pywikibot as pw, sys
from pywikibot.pagegenerators import WikidataSPARQLPageGenerator
from pywikibot.bot import SingleSiteBot


class WikidataQueryBot(SingleSiteBot):
    def __init__(self, generator, source_lang, source_text, target_lang, target_text, **kwargs):
        super(WikidataQueryBot, self).__init__(**kwargs)
        self.generator = generator
        self.source_lang = source_lang
        self.source_text = source_text
        self.target_lang = target_lang
        self.target_text = target_text

    def treat(self, item):
        item.editDescriptions(descriptions={self.target_lang: self.target_text},
                              summary=u'+{}:{} based on {}:{}'.format(self.target_lang,
                                                                      self.target_text,
                                                                      self.source_lang,
                                                                      self.source_text))
        print("Saving {}".format(str(item)))

if __name__ == '__main__':
    args = sys.argv
    query = """SELECT ?item WHERE {{
  ?item schema:description "{}"@{}.
  FILTER(NOT EXISTS {{
    ?item schema:description ?itemdesc.
    FILTER(LANG(?itemdesc) = "{}") 
  }})
}}""".format(args[1], args[2], args[4])
    print(query)
    site = pw.Site('wikidata', 'wikidata')
    gen = WikidataSPARQLPageGenerator(query, site=site.data_repository(),
                                      endpoint='https://query.wikidata.org/sparql')
    bot = WikidataQueryBot(gen,
                           source_lang=args[2],
                           source_text=args[1],
                           target_lang=args[4],
                           target_text=args[3],
                           site=site)
    bot.run()

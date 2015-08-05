from itertools import chain
from operator import attrgetter
from collections import namedtuple
from multiprocessing.pool import Pool

import feedparser

import config

SearchResult = namedtuple('SearchResult', ['title', 'link'])

pool = Pool(5)

if __name__ == '__main__':
    feeds = pool.imap_unordered(feedparser.parse, config.SEARCH_FEEDS)
    entries = chain.from_iterable(map(attrgetter('entries'), feeds))
    unique_entries = dict((v['link'], v) for v in entries).values()
    results = (SearchResult(entry.title, entry.link) for entry in unique_entries)

from itertools import chain
from operator import attrgetter
from collections import namedtuple
from multiprocessing.pool import Pool

from jinja2 import Environment, FileSystemLoader
import requests
import feedparser

import config

SearchResult = namedtuple('SearchResult', ['title', 'url'])

pool = Pool(5)

if __name__ == '__main__':
    feeds = pool.imap_unordered(feedparser.parse, config.SEARCH_FEEDS)
    entries = chain.from_iterable(map(attrgetter('entries'), feeds))
    unique_entries = dict((v['link'], v) for v in entries).values()
    results = (SearchResult(entry.title, entry.link) for entry in unique_entries)

    if results:
        env = Environment(autoescape=True, loader=FileSystemLoader('templates'))
        template = env.get_template('notification.html')
        email_msg = template.render(title=config.EMAIL_SUBJECT, results=results)

        requests.post(config.MAILGUN_URL,
                      auth=("api", config.MAILGUN_KEY),
                      data={
                          "from": config.MAILGUN_EMAIL_SENDER,
                          "to": config.SEND_NOTIFICATIONS_TO,
                          "subject": config.EMAIL_SUBJECT,
                          "html": email_msg
                      })

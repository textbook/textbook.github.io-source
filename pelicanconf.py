#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Jonathan Sharpe'
SITENAME = 'textbook'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

THEME = 'starling'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
	('Pelican', 'http://getpelican.com/'),
	('Python.org', 'http://python.org/'),
	('Jinja2', 'http://jinja.pocoo.org/'),
)

# Social widget
SOCIAL = (
	('GitHub', 'https://github.com/textbook'),
    ('Stack Overflow', 'http://stackoverflow.com/users/3001761/jonrsharpe'),
    ('Twitter', 'https://twitter.com/jonrsharpe'),
)

DISQUS_SITENAME = 'textbook-dev'
GITHUB_URL = 'https://github.com/textbook/textbook.github.io-source'
GOOGLE_ANALYTICS = 'UA-64837080-1'

STATIC_PATHS = [
	'images', 
	'extra/robots.txt', 
	'extra/favicon.ico'
]
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

TYPOGRIFY = True

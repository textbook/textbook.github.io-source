#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Jonathan Sharpe'
SITENAME = 'textbook'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

THEME = 'notmyidea'

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
	('You can add links in your config file', '#'),
    ('Another social link', '#'),
)

STATIC_PATHS = [
	'images', 
	# 'extra/robots.txt', 
	'extra/favicon.ico'
]
EXTRA_PATH_METADATA = {
    #'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

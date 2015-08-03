#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Base configuration
AUTHOR = 'Jonathan Sharpe'
AVATAR = 'avatar.jpg'
SITENAME = 'textbook'
SITESUBTITLE = "These are my opinions - if you don't like them, I have others"
PATH = 'content'
TIMEZONE = 'Europe/London'
DEFAULT_LANG = 'en'

# Appearance
THEME = 'meadowlark'
TYPOGRIFY = True
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['assets']
JINJA_EXTENSIONS = ['webassets.ext.jinja2.AssetsExtension']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
	('Atom IDE', 'http://blog.atom.io/'),
	('Campo Santo', 'http://blog.camposanto.com/'),
	('Code as Craft', 'https://codeascraft.com/'),
)

# Social widget
SOCIAL = (
	('BitBucket', 'https://bitbucket.org/jonrsharpe'),
	('GitHub', 'https://github.com/textbook'),
    ('Stack Overflow', 'http://stackoverflow.com/users/3001761/jonrsharpe'),
    ('Twitter', 'https://twitter.com/jonrsharpe'),
)

# Other settings
#DISQUS_SITENAME = 'textbook-dev'
GITHUB_URL = 'https://github.com/textbook/textbook.github.io-source'
#GOOGLE_ANALYTICS = 'UA-64837080-1'
TWITTER_USERNAME = 'jonrsharpe'

# Static files
STATIC_PATHS = [
	'images',
	'extra/robots.txt',
	'extra/favicon.ico'
]
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

DEFAULT_PAGINATION = 4

# URL settings
# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
ARTICLE_SAVE_AS = '{date:%Y}/{date:%b}/{date:%d}/{slug}.html'
ARTICLE_URL = '{date:%Y}/{date:%b}/{date:%d}/{slug}.html'
# Don't need the author pages
AUTHOR_SAVE_AS = ''
AUTHOR_URL = ''
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'

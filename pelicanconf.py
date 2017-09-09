#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import bulrush

# Base configuration
AUTHOR = 'Jonathan Sharpe'
AVATAR = 'avatar.png'
SITENAME = 'textbook'
SITESUBTITLE = "These are my opinions - if you don't like them, I have others"
PATH = 'content'
TIMEZONE = 'Europe/London'
DEFAULT_LANG = 'en'

# Appearance
THEME = bulrush.PATH
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['assets']
JINJA_ENVIRONMENT = bulrush.ENVIRONMENT
JINJA_FILTERS = bulrush.FILTERS

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ('Pivotal Engineering Journal', 'http://engineering.pivotal.io/'),
    ('The Clean Code Blog', 'http://blog.cleancoder.com/'),
    ('Code as Craft', 'https://codeascraft.com/'),
    ('Corgibytes Blog', 'http://corgibytes.com/blog/'),
)

# Social widget
SOCIAL = (
    ('GitHub', 'https://github.com/textbook'),
    ('Stack Overflow', 'http://stackoverflow.com/users/3001761/jonrsharpe'),
    ('Twitter', 'https://twitter.com/jonrsharpe'),
    ('500px', 'https://500px.com/jonrsharpe'),
)

# Other settings
GITHUB_URL = 'https://github.com/textbook/textbook.github.io-source'
TWITTER_USERNAME = 'jonrsharpe'
MAILCHIMP = dict(
    domain='jonrshar.us15.list-manage.com',
    user_id='7ada11180797f3af73228bf0b',
    list_id='d172abcbd2',
    rewards_url='http://eepurl.com/cNv6Rb',
)
LICENSE = 'CC BY-SA 4.0'

DELETE_OUTPUT_DIRECTORY = True
OUTPUT_RETENTION = ['.git', '.gitignore']

# Static files
STATIC_PATHS = [
    'images',
    'extra',
]
EXTRA_PATH_METADATA = {
    'extra/custom.css': {'path': 'custom.css'},
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/CNAME': {'path': 'CNAME'},
    'extra/LICENSE': {'path': 'LICENSE'},
    'extra/README': {'path': 'README'},
}
# IGNORE_FILES = ['.#*', 'README.md']

DEFAULT_PAGINATION = 5

# URL settings
SLUGIFY_SOURCE = 'basename'
# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
ARTICLE_SAVE_AS = '{date:%Y}/{date:%b}/{date:%d}/{slug}.html'
ARTICLE_URL = '{date:%Y}/{date:%b}/{date:%d}/{slug}.html'
# Don't need the author pages
AUTHOR_SAVE_AS = ''
AUTHOR_URL = ''
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'

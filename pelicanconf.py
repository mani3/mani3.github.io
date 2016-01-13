#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'mani3'
SITENAME = u'Lavieleaf'
SITEURL = ''
THEME = 'pelican-bootstrap3'
#DIRECT_TEMPLATES = (('index', 'archives', '404'))

BOOTSTRAP_THEME = 'sandstone'
#PLUGIN_PATHS = ['./pelican-plugins']
#PLUGINS = ['assets']

BS3_URL = 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css'
BS3_JS  = 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js'
BS3_THEME = 'http://bootswatch.com/slate/bootstrap.min.css'

PATH = 'content'

TIMEZONE = 'Asia/Tokyo'

DEFAULT_LANG = u'ja'

ARTICLE_URL = 'posts/{date:%Y}/{date:%b}/{date:%d}/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/{date:%d}/{slug}.html'
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'
TAGS_URL = 'tags.html'
TAGS_SAVE_AS = TAGS_URL
TAG_CLOUD_STEPS = 4
TAG_CLOUD_MAX_ITEMS = 100
DEFAULT_CATEGORY = ''

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('github', 'http://github.com/mani3'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

AUTHORS = {
    u'mani3': '/about.html',
}

DATE_FORMATS = {
    'en': ('en_US','%a, %d %b %Y'),
    'jp': ('ja_JP','%Y-%m-%d(%a)'),
}

STATIC_PATHS = [
    'images',
 #   'extra/robots.txt',
    'extra/favicon.ico'
]

EXTRA_PATH_METADATA = {
#    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

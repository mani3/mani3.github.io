#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'mani3'
SITENAME = u'Lavieleaf'
SITEURL = ''
SITESUBTITLE = 'おもったことをなんでも書くことろ'

THEME = 'pelican-alchemy/alchemy'
PYGMENTS_STYLE = 'paraiso-dark'

PATH = 'content'

TIMEZONE = 'Asia/Tokyo'

DEFAULT_LANG = u'ja'

ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
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
# LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
    ('github', 'http://github.com/mani3'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

AUTHORS = {
    u'mani3': '/about.html',
}

ICONS = (
    ('github', 'https://github.com/mani3'),
)

DATE_FORMATS = {
    'en': ('en_US', '%a, %d %b %Y'),
    'jp': ('ja_JP', '%Y-%m-%d(%a)'),
}

STATIC_PATHS = [
    'images',
    'extra/robots.txt',
    'extra/favicon.ico',
    'perspective-correction',
]

EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'perspective-correction/index.html': {'path': 'perspective-correction/index.html'}
}

GOOGLE_ANALYTICS = 'UA-26392156-5'

PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = ['pelican_advance_embed_tweet', 'render_math']

READERS = {"html": None}

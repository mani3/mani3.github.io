AUTHOR = 'mani3'
SITENAME = 'Lavieleaf'
SITESUBTITLE = 'おもったことをなんでも書くことろ'
SITEURL = 'https://mani3.github.io'

THEME = 'pelican-alchemy/alchemy'
PYGMENTS_STYLE = 'paraiso-dark'

PATH = 'content'

TIMEZONE = 'Asia/Tokyo'

DEFAULT_LANG = 'ja'
ARTICLE_URL = 'posts/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{slug}.html'
# TAG_URL = 'tag/{slug}/'
# TAG_SAVE_AS = 'tag/{slug}/index.html'
# TAGS_URL = 'tags.html'
# TAGS_SAVE_AS = TAGS_URL
# TAG_CLOUD_STEPS = 4
# TAG_CLOUD_MAX_ITEMS = 100
# DEFAULT_CATEGORY = ''

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('Pelican', 'https://getpelican.com/'),
#          ('Python.org', 'https://www.python.org/'),
#          ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
  ('github', 'http://github.com/mani3'),
)

DEFAULT_PAGINATION = 10

AUTHORS = {
    u'mani3': '/about.html',
}

ICONS = (
    ('github', 'https://github.com/mani3'),
)

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

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

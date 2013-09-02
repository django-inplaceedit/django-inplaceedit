import sys

if sys.version_info.major == 2:
    from .news_py2 import *
else:
    from .news_py3 import *

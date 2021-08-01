# 单独做一个cache.py，是为了防止视图函数和工厂函数循环引用
# 工厂函数从cache.py引用，视图函数/资源路由从cache.py里引用，这样就不会循环引用了
from flask_caching import Cache

cache = Cache()
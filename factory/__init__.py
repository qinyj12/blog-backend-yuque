import os
from flask import Flask
from flask_mail import Mail

def creat_app(spare_config = None):
    # 自定义实例文件夹/resource，此处为绝对路径，可以通过其他参数改为相对路径
    # 和模板文件夹/template，此处为相对路径
    # ################################# static_folder，好像通过这个参数可以让外部访问这个文件夹
    app = Flask(
        __name__, 
        instance_path = '/resource', 
        # template_folder = '../template',  # 这是模板的路径
        # 默认的static目录是'/factory/static'，这里改成'/static'
        static_folder = os.path.join(os.getcwd(), 'static')
        # static_url_path = '/static'
    )

    # 如果creat_app()没有接收到参数，使用默认的config文件
    if spare_config is None:
        from .config import config
        app.config.from_object(config.Config)

    # 否则，使用参数中的config文件
    else:
        app.config.from_pyfile(spare_config)

    # 从cache.py中引入cache对象
    from api.cache import cache
    cache.init_app(app)

    # 引入蓝图
    from resource.yuque import tags as yuque_tags
    app.register_blueprint(yuque_tags.app)

    return app
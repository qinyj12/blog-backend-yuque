from flask import app, Blueprint
from flask_restful import Api, Resource, reqparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from factory.config.secret import Secret
import time
from api.cache import cache

app = Blueprint('YuequeTags', __name__, url_prefix = '/yuque/tags')
api = Api(app)
parser = reqparse.RequestParser()

# 爬虫——获取语雀docs的全部tags
@api.resource('')
class TagsCrawler(Resource):
    # 缓存一天
    @cache.cached(timeout = 86400, key_prefix = 'all_tags')
    def get(self):
        parser.add_argument('login', location = ['args']) # 获取语雀用户名
        args = parser.parse_args()
        yuque_login_name = args['login']

        options = Options()
        options.add_argument('--headless')    # 不打开浏览器
        options.add_argument('--disable-gpu')    # 禁用GPU硬件加速
        options.add_argument('user-agent="Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1"')  # 添加访问头
        # options.add_argument('proxy-server="60.13.42.109:9999"')    # 添加代理
        driver = webdriver.Chrome(options=options)   # 使用驱动配置

        try:
            driver.get("https://www.yuque.com/r/" + yuque_login_name + "/tags?tag=") # 打开这个网页，因为没登录，会跳转登录页
            user_name = driver.find_element_by_xpath("//*[@data-aspm-click='d002']") # 获取用户名栏
            user_passwd = driver.find_element_by_xpath("//*[@data-aspm-click='d003']") # 获取密码栏
            login_button = driver.find_element_by_xpath("//*[@data-aspm-click='d009']") # 获取登录按钮
            user_name.send_keys(Secret.YUQUE_ACCOUNT['phone']) # 在用户名栏中输入用户名
            user_passwd.send_keys(Secret.YUQUE_ACCOUNT['password']) # 在密码栏中输入密码
            login_button.click() # 模拟点击登录按钮
            time.sleep(1) # 此时进入新页面，等待Xs
            # 以下为获取到所有docs的标签
            tags_wrapper = driver.find_element_by_class_name('tag-group-wrapper') 
            tags = tags_wrapper.find_elements_by_class_name('tag-title')
            tags_list = [i.text for i in tags] # 把获取到的所有tags放到一个list里
            driver.close()

            return {
                'code': 200,
                'result': tags_list
            }
        except Exception as e:
            return {
                'code': 500,
                'message': e
            }

# 清除tags缓存
@api.resource('/clear')
class TagsCacheClear(Resource):
    def get(self):
        cache.delete('all_tags')
        return {
            'code': 200,
            'result': 'tags缓存清除成功'
        }
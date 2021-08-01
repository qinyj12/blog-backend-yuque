from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')    # 不打开浏览器
    options.add_argument('--disable-gpu')    # 禁用GPU硬件加速
    options.add_argument('user-agent="Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1"')  # 添加访问头
    # options.add_argument('proxy-server="60.13.42.109:9999"')    # 添加代理
    driver = webdriver.Chrome(options=options)   # 使用驱动配置
    driver.get("https://www.yuque.com/r/qinyujie-067rz/tags?tag=") # 打开这个网页，因为没登录，会跳转登录页

    user_name = driver.find_element_by_xpath("//*[@data-aspm-click='d002']") # 获取用户名栏
    user_passwd = driver.find_element_by_xpath("//*[@data-aspm-click='d003']") # 获取密码栏
    login_button = driver.find_element_by_xpath("//*[@data-aspm-click='d009']") # 获取登录按钮

    user_name.send_keys('17611595223') # 在用户名栏中输入用户名
    user_passwd.send_keys('qyj931101') # 在密码栏中输入密码
    login_button.click() # 模拟点击登录按钮
    time.sleep(2) # 此时进入新页面，等待2s
    
    # n = driver.window_handles  # 这个时候会生成一个新窗口或新标签页的句柄，代表这个窗口的模拟driver
    # print('当前句柄: ', n)  # 会打印所有的句柄
    # driver.switch_to_window(n[-1])  # driver切换至最新生产的页面
    
    # 以下为获取到所有docs的标签
    tags_wrapper = driver.find_element_by_class_name('tag-group-wrapper') 
    tags = tags_wrapper.find_elements_by_class_name('tag-title')

    print([i.text for i in tags])

    # tags = driver.find_element_by_class_name('tag-group-wrapper')
    # print(tags)

    driver.implicitly_wait(3)     # 等待时间

    # 将滚动条移动到页面的顶部 0：为顶部；1000000：为底部
    js = "var q=document.documentElement.scrollTop=10000000000"    # js语句
    driver.execute_script(js)    # 执行语句

    driver.close()
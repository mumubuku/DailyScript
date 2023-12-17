from selenium import webdriver
# browsermob-proxy需要运行在java-1.8的环境上
from browsermobproxy import Server

# 启动 browsermob-proxy 服务器
server_options = {
    'port': 8888,
    'use_littleproxy': False  # 启用旧的实现方式
}
server = Server("/Users/mumu/browsermob-proxy-2.1.4/bin/browsermob-proxy", server_options)
print(server)
server.start()
proxy = server.create_proxy()

# 创建带有代理的浏览器实例
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))

driver = webdriver.Chrome(options=chrome_options)

# 开始捕获请求
proxy.new_har("requests")

# 打开页面
driver.get("https://www.baidu.com")

# 输出浏览器发出的请求
for entry in proxy.har['log']['entries']:
    print(entry['request']['url'])

# 关闭浏览器和 server
driver.quit()
server.stop()
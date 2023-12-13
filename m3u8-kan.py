import requests
import random
import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium import webdriver

def get_subdomains():


     url = ''
     with open('data.csv', 'w', newline='') as csvfile:
       writer = csv.writer(csvfile)  
       for number in range(100000, 999999):
        new_url = url.replace('214019', str(number))
       
        driver = webdriver.Chrome()

        driver.get(new_url)


        driver.implicitly_wait(1)

        # 获取需要的元素，这里以获取 div 元素为例
        div_element = driver.find_element(By.ID, 'Player')
        div_html = div_element.get_attribute('src')
        startIndex = div_html.index('url=') + 4
        endIndex = len(div_html)
        result = div_html[startIndex:endIndex]
        print(result)
        driver.quit()  
        
        try:
           writer.writerow([result])
           print('CSV文件写入成功')
        except Exception as e:
           print('CSV文件写入失败，错误信息：', e)
           

  
                   


url = 'https://www.imooc.com/course/list'
subdomains = get_subdomains()

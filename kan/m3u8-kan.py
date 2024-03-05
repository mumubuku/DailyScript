import requests
import random
import os
import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
import sys

def get_subdomains(arg1,arg2):


   url = 'https://www.kan9132.com/vodplay/214019-1-1.html'

     # 读取文件中的数字
   if os.path.exists(arg1+'num.txt'):
     with open('num.txt', 'r') as f:
      num = int(f.read())
      print(num)
   else:
     with open('num.txt','w') as f:
       f.write('100000')
   
   with open('data.csv', 'a', newline='') as csvfile:
       writer = csv.writer(csvfile)  
       for number in range(arg1, arg2):
        new_url = url.replace('214019', str(number))
        with open('num.txt','w') as f:
         f.write(str(number))
       
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = Chrome(options=chrome_options)      

        driver.get(new_url)


        driver.implicitly_wait(1)

        # 获取需要的元素，这里以获取 div 元素为例
        div_element = driver.find_element(By.ID, 'Player')
        div_html = div_element.get_attribute('src')
        startIndex = div_html.index('url=') + 4
        endIndex = len(div_html)
        result = div_html[startIndex:endIndex]
        print(result)
        

        div_element = driver.find_element(By.NAME, 'description')
        print(div_element)
        content = div_element.get_attribute('content')
        print(content)
        
        
        driver.quit()  
        try:
           writer.writerow([content,result])
           print('CSV文件写入成功')
        except Exception as e:
           print('CSV文件写入失败，错误信息：', e)
           

  
                   


url = 'https://www.imooc.com/course/list'
arg1 = sys.argv[1]
arg2 = sys.argv[2]
subdomains = get_subdomains(arg1,arg2)

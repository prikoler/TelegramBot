import time
from bs4 import BeautifulSoup
from selenium import webdriver
from sql import SQLite

db = SQLite('database.db')

class Parser:
    def result(self):
        driver = webdriver.Chrome()
        url = 'https://qiwi.com/payment/exchange'
        driver.get(url)
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.findAll('p', class_='css-xk1yoo')
        res = [c.text for c in divs]
        driver.quit()
        return res

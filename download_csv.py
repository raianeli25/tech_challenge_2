from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def download():
    driver = webdriver.Chrome()

    try:

        driver.get('https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br')

        downloadcsv= driver.find_element(By.LINK_TEXT, "Download")
        
        downloadcsv.click()

        time.sleep(10)    

        driver.close()

        return print("CSV baixado")

    except:

        return print("Invalid URL")
    



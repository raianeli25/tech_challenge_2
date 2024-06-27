from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

def download():
    driver = webdriver.Chrome()

    try:

        driver.get('https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br')

        webwait = WebDriverWait(driver, 10)

        element = webwait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="segment"]/option[2]')
                )
            )
        element.click()
        driver.execute_script("arguments[0]", element)
        time.sleep(10)

        downloadcsv= driver.find_element(By.LINK_TEXT, "Download")
        
        downloadcsv.click()

        time.sleep(10)    

        driver.close()

        return print("CSV baixado")

    except:

        return print("Invalid URL")
    



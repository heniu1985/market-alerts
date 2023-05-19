import time
import os

from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from dotenv import load_dotenv
from twocaptcha import TwoCaptcha


URL = 'https://stooq.pl/db/h/'

# chrome_options = Options()
# chrome_options.add_argument('--headless=chrome')

driver = webdriver.Chrome(
    executable_path='data_downloader/chromedriver',
    # options=chrome_options
)
driver.get(URL)
driver.maximize_window()

time.sleep(5)

cookie_button = driver.find_element(
    By.XPATH,
    '/html/body/div/div[2]/div[1]/div[2]/div[2]/button[1]/p'
)
cookie_button.click()

time.sleep(5)

download_link = driver.find_element(
    By.XPATH,
    '/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr[2]/td[1]/table/tbody/tr[5]/td[3]/a'
)
download_link.click()

time.sleep(5)

captcha_img = driver.find_element(By.ID, "cpt_cd")

with open('data_downloader/captcha.png', 'wb') as captcha:
    captcha.write(captcha_img.screenshot_as_png)

load_dotenv()
API_KEY = os.getenv('API_KEY')
solver = TwoCaptcha(API_KEY)

captcha_solve = solver.normal('data_downloader/captcha.png')
id = solver.send(file='data_downloader/captcha.png')

time.sleep(45)

code = solver.get_result(id)

captcha_text = driver.find_element(
    By.XPATH,
    '/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table[5]/tbody/tr/td/div[1]/div[1]/table/tbody/tr/td/table/tbody/tr[5]/td/input'
)
captcha_text.send_keys(code)

captcha_button = driver.find_element(
    By.XPATH,
    '/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table[5]/tbody/tr/td/div[1]/div[1]/table/tbody/tr/td/table/tbody/tr[6]/td/input'
)
captcha_button.click()

time.sleep(5)

download_button = driver.find_element(By.ID, "cpt_gt")
download_button.click()

time.sleep(90)
driver.close()

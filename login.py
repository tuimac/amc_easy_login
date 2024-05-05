from boto3 import client
from setup import Setup
from traceback import format_exc
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def get_sts_token():
    sts = client('sts')
    sts.assume_role()

def setup() -> str:
    try:
        setup = Setup()
        setup.selenium()
        global webdriver_path
        webdriver_path = setup.webdriver_path
    except:
        raise

def access():
    try:
        options = ChromeOptions()
        options.add_argument('--user-data-dir=C:\\Users\\kento\\Downloads\\test')
        options.add_argument('--profile-directory=Default')
        options.add_experimental_option('detach', True)
        options.add_experimental_option("excludeSwitches", ['enable-automation', 'load-extension'])
        driver = Chrome(options=options)
        driver.execute_script("window.open('about:blank', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get('https://sites.google.com/chromium.org/driver/')
        driver.quit()
    except:
        raise
        

if __name__ == '__main__':
    try:
        setup()
        access()
    except:
        print(format_exc())
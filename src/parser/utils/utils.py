import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def get_fresh_cookies_and_headers(url):
    """Получение свежих cookies и заголовков."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    service = Service('/usr/local/bin/chromedriver')

    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(url)
        time.sleep(5)

        selenium_cookies = driver.get_cookies()
        cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}

        headers = {
            'User-Agent': driver.execute_script("return navigator.userAgent;"),
            'Accept': (
                'text/html,application/xhtml+xml,application/xml;q=0.9,'
                'image/avif,image/webp,image/apng,*/*;q=0.8,'
                'application/signed-exchange;v=b3;q=0.7'
            ),
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': driver.execute_script("return navigator.language;"),
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        return cookies, headers
    finally:
        driver.quit()

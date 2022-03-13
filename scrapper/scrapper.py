import time
import os
from gsp.gsp import write
import datetime
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

month_map = {
    'jan': 1,
    'feb': 2,
    'mar': 3,
    'apr': 4,
    'may': 5,
    'jun': 6,
    'jul': 7,
    'aug': 8,
    'sep': 9,
    'oct': 10,
    'nov': 11,
    'dec': 12
}

chrome_options = Options()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('window-size=200,200')


def formatDate(date):
    if date.strip() == "":
        datetime.date(2000, 1, 1)
    day, month, year = date.split()
    day = int(day)
    month = int(month_map[month.strip()[:3].lower()])
    year = int(re.sub("'", "20", year))
    return datetime.date(year, month, day)


class Scraper(webdriver.Chrome):
    def __init__(self, driver_path=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),
                                                    options=chrome_options), teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        super(Scraper, self).__init__()
        self.implicitly_wait(2500)

    def login(self, email, password):
        self.get("https://app.ahrefs.com/user/login")
        self.implicitly_wait(25)
        self.find_element(
            By.XPATH, "//input[@name='email']").send_keys(email)
        self.find_element(
            By.XPATH, "//input[@name='password']").send_keys(password)
        self.find_element(
            By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(self, 30).until(
            ec.url_matches('https://app.ahrefs.com/dashboard'))
        print("logged in")

    def scrape(self, target, last_domain, last_date):
        dr = 1
        all_links = []
        self.get(f'https://app.ahrefs.com/site-explorer/others/v2/linked-domains/subdomains/live/all/all/1'
                 f'/first_seen_desc?target={target}')
        time.sleep(5)
        print(self.current_url)
        print(self.get_window_size())
        self.refresh()
        # Check for if it gets logged out
        if self.current_url == "https://app.ahrefs.com/sessions-exceeded":
            print("Logged out! Logging in...")
            self.login('rahulthepcl@gmail.com', 'Adsense007##')
            self.scrape(target, last_date, last_domain)

        print(self.current_url)
        total_number = self.find_element(
            By.ID, 'result_info').find_element(By.TAG_NAME, "var").text
        total_number = int(re.sub(r"\D", "", total_number))
        print(total_number)
        updated_link = self.find_elements(
            By.XPATH, '//tbody/tr/td[1]//a[@href]')[0].get_attribute("href")
        updated_date = self.find_elements(
            By.XPATH, '//tbody/tr/td[10]')[0].text

        while len(all_links) < total_number:

            self.get(
                f'https://app.ahrefs.com/site-explorer/others/v2/linked-domains/subdomains/live/all/all/{dr}/first_seen_desc?target={target}')
            self.implicitly_wait(10)

            # Check for if it gets logged out
            if self.current_url == "https://app.ahrefs.com/sessions-exceeded":
                print("Logged out! Logging in...")
                self.login('rahulthepcl@gmail.com', 'Adsense007##')
                self.scrape(target, last_date, last_domain)

            link = self.find_elements(
                By.XPATH, '//tbody/tr/td[1]//a[@href]')
            date = self.find_elements(
                By.XPATH, '//tbody/tr/td[10]')

            for index in range(len(link)):
                tmp1 = link[index].get_attribute("href")
                tmp2 = date[index].text

                if tmp1 == last_domain or formatDate(tmp2) < formatDate(last_date):
                    write(all_links)
                    time.sleep(2.1)
                    print(updated_date)
                    return [updated_link, updated_date]

                all_links.append([tmp1])
                # print(tmp1)

            self.implicitly_wait(10)

            if len(link) % 50 == 0 and len(link) != 0:
                dr += 1

        write(all_links)
        time.sleep(2.1)
        # print(updated_date)
        return [updated_link, updated_date]

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

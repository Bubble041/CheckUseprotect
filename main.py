from tkinter.tix import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
import csv
import os
import datetime

def get_html_Uceprotect(url, pool, number):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument('headless')
    browser = webdriver.Chrome(executable_path=r'chromedriver.exe', chrome_options=options)
    browser.get(url)
    time.sleep(2)

    select_ip = Select(browser.find_element_by_name('whattocheck'))
    select_ip.select_by_value(pool)

    asn_input = browser.find_element_by_name('ipr')
    asn_input.clear()
    asn_input.send_keys(number)

    asn_input.send_keys(Keys.ENTER)
    time.sleep(2)

    ip_info = browser.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[2]/center[2]/a')
    ip_info.click()
    time.sleep(2)

    browser.switch_to.window(browser.window_handles[1])
    ip_list = browser.page_source
    with open('index.html', 'w', encoding='utf_8') as file:
        file.write(ip_list)
    print("*****************\nHTML created\n")

def get_info_Uceprotect():

    info = []
    with open('index.html', encoding='utf_8') as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    table = soup.find('table').find('tbody').find_all('tr')
    for data in table[1:]:
        info.append(data)
    
    with open ("data.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["IP", "Impacts", "Latest Impact +/- 1 Minute", "Earliest Expiretime"]
        )
    for data in info:
        with open ("data.csv", "a") as file:
            writer = csv.writer(file, delimiter =",")
            writer.writerow(data)
    print("*****************\nTable created\n")

    newlines = []
    supernewlines = []

    with open ("data.csv", "r") as file:
        lines = file.readlines()
        for line in lines:
            newlines.append(line)
    
    for i in range(len(newlines)):
        line = newlines[i].replace("<td>", "").replace("</td>", "").replace("\n", "")
        if line:
            supernewlines.append(line.strip().split(","))

    today = datetime.datetime.today().strftime("%Y_%m_%d_%H-%M")
    with open (f"data_{today}.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["IP", "Impacts", "Latest Impact +/- 1 Minute", "Earliest Expiretime"]
        )

    for data in supernewlines[2:]:
        with open (f"data_{today}.csv", "a") as file:
            writer = csv.writer(file, delimiter = ",")
            writer.writerow(data)
    print("*****************\nCSV completed\n\n*****************")

def remove_files():
    os.remove("data.csv")
    os.remove("index.html")

def get_csv(base, pool, number):
    if base == "Uceprotect":
        if pool == "ASN":
            get_html_Uceprotect('http://www.uceprotect.net/en/rblcheck.php', pool, number)
            get_info_Uceprotect()
    remove_files()

if __name__ == '__main__':
    get_csv()
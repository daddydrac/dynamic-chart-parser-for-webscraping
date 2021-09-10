from bs4 import BeautifulSoup
import re
import json
import pydash
from selenium import webdriver
from datetime import datetime
import os

#################################################################
# scrape data from dynamic svg based charts and convert to json #
#################################################################


# might need two forward // slashes in front of html
table_e5_xpath = "/html/body/main/article/section[4]/div[1]/table"
table_e4_xpath = "/html/body/main/article/section[4]/div[2]/table"

# web page i want to parse
web_page = 'https://dieselnet.com/standards/us/nonroad.php'

# chromium options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome("/usr/local/bin/chromedriver",
                          chrome_options=chrome_options)


def html_to_list(raw_html: str, _length: int) -> list:


return list(filter(
    lambda arr: len(arr) > _length,
    [[cell.text for cell in row("td")]
     for row in BeautifulSoup(raw_html, features="lxml")("tr")
     ]
))


def html_map(callback, html_data: dict) -> list:


return list(map(lambda current: callback(current), html_data))


def custom_cleaning(current, idx, arr):


if len(current) < 7 and idx > 0:
current.insert(0, str(arr[idx-1][0]))
return current


def page_setup(_url, _xpath):


driver.get(_url)
tbl = driver.find_element_by_xpath(_xpath).get_attribute('outerHTML')
return tbl


#################################################################
# get e5 table and create custom mapper

def e5_mapper(current):


return {
    "EnginePower": re.sub('\u00a0', ' ', re.sub('\u2264', '<=', current[0])),
    "Year": current[1],
    "CO": current[2],
    "NMHC": current[3],
    "NMHC+NO": current[4],
    "NO": current[5],
    "PM": current[5],
}

e5_result = html_map(
    e5_mapper,
    pydash.collections.map_(
        html_to_list(
            page_setup(web_page, table_e5_xpath), 1),
        lambda current, idx, arr:
        custom_cleaning(current, idx, arr)
    )
)


print(json.dumps({"e5_table": e5_result}, indent=4))
print("-----------------------------------------------------------")

####################################################################
# get e4 table and create custom mapper


def e4_mapper(current):


return {
    "YEAR": current[0],
    "CATEGORY": current[1],
    "CO": current[2],
    "NHMC": current[3],
    "NOx": current[4],
    "PM": current[5]
}

e4_result = html_map(
    e4_mapper,
    pydash.collections.map_(
        html_to_list(
            page_setup(web_page, table_e4_xpath), 1),
        lambda current, idx, arr:
        custom_cleaning(current, idx, arr)
    )
)

print(json.dumps({"e4_table": e4_result}, indent=4))


import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import urllib.request
import pathlib
import os


def scroll_webpage(driver, times):
    SCROLL_PAUSE_TIME = 1
    count = 0

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while count < times:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        count += 1


def extract_userinput(query):

    # Extract user-input
    url = "https://unsplash.com/search/photos/" + \
        query if len(query) > 1 else "https://unsplash.com"
    return url


def extract_data(browser, url, scroll, css_selector):
    browser.get(url)
    if 'collections/' in url:
        load_more(browser)
        time.sleep(5)
    scroll_webpage(browser, scroll)
    time.sleep(2)
    return browser.find_elements_by_css_selector(css_selector)


def extract_and_save_imgs(browser, img_url, scroll, result_folder):
    # Save img
    # Make folder
    pathlib.Path(result_folder).mkdir(parents=True, exist_ok=True)
    a_selector = "a[itemprop='contentUrl']"
    imgs = extract_data(browser, img_url, scroll, a_selector)
    src = []
    for img in imgs:
        img_id = img.get_attribute('href').split('/')[-1]
        src.append('https://unsplash.com/photos/' +
                   img_id + '/download?force=true')
    browser.get(src[0])
    for url in src[1:]:
        browser.execute_script('window.open("{}", "_blank");'.format(url))


def extract_href_and_name(browser, scroll):
    collections_href_selector = "div[data-test='collection-feed-card'] div:nth-child(1) div a"
    collections_url = 'https://unsplash.com/collections'
    # Selectors

    name = []
    href = []

    collections_href = extract_data(
        browser, collections_url, scroll, collections_href_selector)
    for collection in collections_href:
        url = collection.get_attribute('href')
        if url not in href:
            href.append(url)
            url_split = url.split('/')[-1].split('-')
            title = ''
            for url_s in url_split:
                title += url_s + ' '
            name.append(title.title().strip())

    return name, href


def load_more(browser):
    button = browser.find_element_by_xpath(
        "//button[@class='_37zTg _1l4Hh _1CBrG _3TTOE NDx0k _2Xklx']")
    browser.execute_script("arguments[0].click();", button)

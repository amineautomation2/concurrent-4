from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from utils import delay, find_element_or_none, get_with_backoff


def get_fidelity_keyword(driver: WebDriver, data: list[dict]) -> list[dict]:
    keyword_xpath_p = "//span[contains(., 'can be held')]"
    wait = WebDriverWait(driver, timeout=5)
    for fund in data:
        url = fund["url"]
        try:
            get_with_backoff(driver, url)
        except:
            print("error: ", url)
            continue
        keyword = find_element_or_none(wait, keyword_xpath_p)
        if keyword:
            fund.update(dict(keyword=keyword.text.strip()))
        delay(1, 3)
    return data

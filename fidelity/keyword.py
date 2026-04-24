from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from utils import delay, find_element_or_none


def get_fidelity_keyword(driver: WebDriver, data: list[dict]) -> list[dict]:
    keyword_xpath_p = "//span[contains(., 'can be held')]"
    wait = WebDriverWait(driver, timeout=5)
    for fund in data:
        url = fund["url"]
        try:
            # get_with_backoff(driver, url)
            driver.get(url)
        except:
            print("error: ", url)
            fund.update(dict(keyword="-"))
            continue
        keyword = find_element_or_none(wait, keyword_xpath_p)
        if keyword:
            fund.update(dict(keyword=keyword.text.strip()))
        delay(2, 3)
    return data

from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup

GECKODRIVER_PATH = "/usr/bin/geckodriver"

FIREFOX_OPTS = Options()
FIREFOX_OPTS.log.level = "trace"    # Debug
FIREFOX_OPTS.headless = False
    
def main():
    
    link = "https://www.lojaonline.nordestao.com.br/produtos/departamento/acougue/aves"
    
    class_ ="border-promotion"
    
    browser = webdriver.Firefox(
        executable_path=GECKODRIVER_PATH,
        options=FIREFOX_OPTS
    )
    browser.get(link)
    
    # wait for the page to load
    wait = WebDriverWait(browser, 20)
    wait.until(lambda browser: browser.find_element_by_class_name(class_))
    
    elements = browser.find_elements_by_class_name(class_)
    # show the elements
    for element in elements:
        print(element.text)
        print("\n\n")
    
    print(browser.title)
    browser.quit()

if __name__ == "__main__":
    
    main()

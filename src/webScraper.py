from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

class WebScraperCrawler:
    def __init__(
        self, 
        url_base, 
        pages=1, 
        element_class="",
        gecodriver_path = "/usr/bin/geckodriver",
        headless = True
    ):
        """
        Parameters
        ----------
        url_base : str
            Base url to be used in the crawler. It must have a placeholder
        pages : int, optional
            Number of pages to scrap, by default 1
        element_class : str, optional
            Class in the HTML of the elements to be retrieved, by default ""
        gecodriver_path : str, optional
            Path to the geckodriver, by default "/usr/bin/geckodriver"
        headless : bool, optional
            If the browser should be headless, by default True
        """
        self.url_base = url_base
        self.pages = pages
        self.element_class = element_class
        
        self.gecodriver_path = gecodriver_path
        self.headless = headless
        
        self.connect()
        
    def get_urls(self):
        """
        Get the urls to be scrapped

        Returns
        -------
        list of str
            List of urls to be scrapped
        """
        
        urls = []
        for page in range(1, self.pages+1):
            urls.append(self.url_base.format(page))
        return urls
    
    def connect(self):
        """
        Connect to the browser
        """
        
        firefox_opts = Options()
        firefox_opts.log.level = "trace"    # Debug
        firefox_opts.headless = self.headless

        self.browser = webdriver.Firefox(
            executable_path=self.gecodriver_path,
            options=firefox_opts
        )
    
    def get_elements(self, url, element_class):
        """
        Get the elements from the url that match the element_class
        specified.

        Parameters
        ----------
        url : str
            Url to be scrapped
        element_class : str
            Class in the HTML of the elements to be retrieved

        Returns
        -------
        list of selenium.webdriver.firefox.webelement.FirefoxWebElement
            List of elements that match the element_class
        """
        
        print(f"Getting elements from {url}")
        self.browser.get(url)
        
        try:
            # wait for the page to load
            wait = WebDriverWait(self.browser, 30)
            wait.until(
                lambda browser: browser.find_element_by_class_name(element_class)
            )
            
            elements = self.browser.find_elements_by_class_name(element_class)
        except Exception as e:
            print(f"Error: {e}")
            elements = []
        
        return elements
    
    def get_data(self):
        """
        Run the scrap and returns the data.
        It consists of a list of str, containing the text of each element found.

        Returns
        -------
        list of str
            The text of all the elements found in the page
        """
        urls = self.get_urls()
        
        elements = []
        for url in urls:
            elements+= [
                        self.extract_data_from_element(element) 
                        for element 
                        in self.get_elements(url, self.element_class)
                    ]
        return elements
    
    def extract_data_from_element(self, element):
        """
        Extract the data from the element

        Parameters
        ----------
        element : selenium.webdriver.firefox.webelement.FirefoxWebElement
            Element to be scrapped 

        Returns
        -------
        str
            Text of the element
        """
        return element.text
    
    def quit(self):
        """
        Quit the browser
        """
        self.browser.quit()
    

class WebScrapperCaption( WebScraperCrawler ):
    
    def extract_data_from_element(self, element):
        """
        Extract the data from the element

        Parameters
        ----------
        element : selenium.webdriver.firefox.webelement.FirefoxWebElement
            Element to be scrapped 

        Returns
        -------
        str
            Text of the element
        """
        
        title_class = "caption"
        
        # find div with class "caption"
        title = element.find_element_by_class_name(title_class)
        
        # find the text
        return title.text + " " + element.text
    

if __name__ == "__main__":
    
    url_base = "https://www.lojaonline.nordestao.com.br/produtos/departamento/acougue/aves?page={}"
    element_class = "border-promotion"
    
    crawler = WebScrapperCaption(url_base, pages=2, element_class=element_class)
    data = crawler.get_data()
    print(data)
    
    crawler.quit()
from nis import match
from webScraper import WebScraperCrawler, WebScrapperCaption
import re

import pprint

def extract_price(text):
    # Format r$ 20,00
    price = re.findall(r"R\$ \d+,\d+", text)[0]
    price = price.replace("R$", "").replace(",", ".").strip()
    return float(price)

def extract_peso(text):
    # Format 1,5kg or 100g
    
    matches = re.findall(
        r"\d+(?:,\d+){0,1}\s{0,1}kg|\d+g", 
        text.lower()
    )
    
    if len(matches) == 0:
        return None

    peso = matches[-1]
    
    if "kg" in peso:
        peso = peso.replace("kg", "").replace(",", ".")
        return float(peso)*1000
    else:
        peso = peso.replace("g", "")
        return float(peso)
    
def extract_name(text):
    # Format: name 100g
    name = re.findall(r"\D+", text)[0]
    return name


if __name__ == "__main__":
    NUMBER_OF_PAGES = 2
    urls_base = [
        "https://www.lojaonline.nordestao.com.br/produtos/departamento/acougue/aves?page={}",
        "https://www.lojaonline.nordestao.com.br/produtos/departamento/acougue/peixes?page={}",
        "https://www.lojaonline.nordestao.com.br/produtos/departamento/acougue/bovinos?page={}",
        "https://www.lojaonline.nordestao.com.br/produtos/departamento/acougue/suinos?page={}",
    ]
    element_class = "border-promotion"
    
    for url_base in urls_base:
        crawler = WebScrapperCaption(
            url_base, 
            pages=NUMBER_OF_PAGES, 
            element_class=element_class
        )
        elements = crawler.get_data()
        crawler.quit()
        
        data = [
            {
                "price": extract_price(text),
                "peso": extract_peso(text),
                "nome": extract_name(text),
                "text": text,
                "tipo": url_base.split("/")[-2],
            }
            for text in elements
        ]
        
    pprint.pprint(data)
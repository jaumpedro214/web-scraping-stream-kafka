from webScraper import WebScrapperCaption

import re
import hashlib
import pprint

import json
from confluent_kafka import Producer

def extract_price(text):
    # Format r$ 20,00
    matches = re.findall(r"R\$ \d+,\d+", text)
    
    if len(matches) == 0:
        return None
    
    price = matches[0]
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
    
    # ==================================================================
    #                   Configuring initial parameters
    # ==================================================================
    
    
    # Define the urls to be scrapped
    NUMBER_OF_PAGES = 2
    urls_base = [
        "https://www.lojaonline.nordestao.com.br/produtos/departamento/acougue/aves?page={}",
        "https://www.lojaonline.nordestao.com.br/produtos/departamento/acougue/peixes?page={}",
        "https://www.lojaonline.nordestao.com.br/produtos/departamento/acougue/bovinos?page={}",
        "https://www.lojaonline.nordestao.com.br/produtos/departamento/acougue/suinos?page={}",
    ]
    element_class = "border-promotion"
    
    # Instantiate kafka producer
    TOPIC = "produtos"
    PRODUCT_SCHEMA = {
        "type": "struct",
        "fields": [
            {"type": "string", "optional": False, "field": "id"},
            {"type": "string", "optional": True, "field": "nome"},
            {"type": "float", "optional": True, "field": "price"},
            {"type": "float", "optional": True, "field": "peso"},
            {"type": "string", "optional": True, "field": "text"},
            {"type": "string", "optional": True, "field": "tipo"},
        ],
        "optional": False,
        "name": "produto"
    }
    producer = Producer({
        "bootstrap.servers": "localhost:9092",
        "client.id": "webScraper",
    })
    
    
    # ==================================================================
    #                       Scraping the data
    # ==================================================================
    
    for url_base in urls_base:
        print("Crawling: ", url_base)
        crawler = WebScrapperCaption(
            url_base, 
            pages=NUMBER_OF_PAGES, 
            element_class=element_class,
            headless=True
        )
        elements = crawler.get_data()
        crawler.quit()
        
        print("Found {} elements".format(len(elements)))
        
        data = [
            {
                "price": extract_price(text),
                "peso": extract_peso(text),
                "nome": extract_name(text),
                "text": text,
                "tipo": url_base.split("/")[-2],
                "id": str(hashlib.sha1(text.encode()).hexdigest())
            }
            for text in elements
        ]
        
        # Transform data into AVRO format
        # Send to Kafka
        print("Sending to Kafka")
        for item in data:
            pprint.pprint(item)
            # Transform data into AVRO format
            producer.produce(
                TOPIC,
                value=json.dumps(
                    {
                        "schema": PRODUCT_SCHEMA, 
                        "payload": item
                    }
                )
            )
            producer.flush()
            
    
    print( "Done" )
from webScraper import WebScrapperCaption
from extract_functions import extract_name, extract_price, extract_peso

import hashlib
import pprint

import json
from confluent_kafka import Producer

import argparse
import time

if __name__ == "__main__":
    
    # Parse arguments
    # ==================================================================
    # NUMBER_OF_PAGES int, default 2
    # KAFKA_SERVER str, default localhost:9092
    
    parser = argparse.ArgumentParser(
        description="Scraping data from a website and insert into kafka"
    )
    
    parser.add_argument(
        "--number-of-pages",
        type=int,
        default=2,
        help="Number of pages to scrap"
    )

    parser.add_argument(
        "--kafka-server",
        type=str,
        default="localhost:9092",
        help="Kafka server address"
    )
    
    NUMBER_OF_PAGES = parser.parse_args().number_of_pages
    KAFKA_SERVER = parser.parse_args().kafka_server
    
    print("Number of pages: {}".format(NUMBER_OF_PAGES))
    print("Kafka server: {}".format(KAFKA_SERVER))
    time.sleep(30)
    
    
    # Configuring initial parameters
    # ==================================================================
    
    
    # Define the urls to be scrapped
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
        "bootstrap.servers": KAFKA_SERVER,
        "client.id": "webScraper",
    })
    
    
    # Scraping the data
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
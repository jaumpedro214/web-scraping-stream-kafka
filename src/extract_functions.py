import re

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
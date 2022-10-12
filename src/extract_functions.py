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
        r"[^$]{2}\s+(\d+(?:,\d+){0,1}\s{0,1}kg|\d+g)", 
        text.lower()
    )
    
    if len(matches) == 0:
        return None

    # Store in grams
    # the highest value found
    peso = 0
    for match in matches:
        if "kg" in match:
            match = match.replace("kg", "").replace(",", ".")
            peso_match = float(match) * 1000
        else:
            match = match.replace("g", "")
            peso_match = float(match)
        
        if peso_match > peso:
            peso = peso_match
    
    return peso
    
def extract_name(text):
    # All the text before the first number
    name = re.findall(r"\D+", text)[0]
    return name
import re

def verify_phone_number(phone_number):
    pattern = r'^\+?(\d{1,4})?[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'
    return re.match(pattern, phone_number) is not None

def verify_address(address):
    pattern = r'\d{1,4} [a-z\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd)\W?(?=[^\w\s,]|$)'
    return re.match(pattern, address, re.IGNORECASE) is not None

def verify_website_link(link):
    pattern = r'^https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^/#?]+)*/?$'
    return re.match(pattern, link) is not None

def extract_phone_number_after_split(text):
    pattern = r'Phone:|Call:|Call us:|Telephone:|Cell:|Cellphone:|Mobile:'
    match = re.search(pattern, text)
    if match:
        phone_number_text = text[match.end():].strip()
        if verify_phone_number(phone_number_text[:11]):
            return phone_number_text[:11]
    else:
        return None 
    
def extract_address_after_split(text):
    pattern = r'Address:|Location:'
    match = re.search(pattern, text)
    if match:
        address_text = text[match.end():].strip()
        if verify_address(address_text[:15]):
            return address_text[:15]
    else:
        return None

    


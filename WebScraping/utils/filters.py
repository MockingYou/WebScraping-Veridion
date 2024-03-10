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
    pattern = r'Phone:|Call:|Call us:|Telephone:|T:'
    if re.search(pattern, text):
        split_text = re.split(pattern, text)
        phone_number_text = split_text[-1].strip()
        return phone_number_text[-11:]
    else:
        return None 
    
def extract_address_after_split(text):
    pattern = r'Address:|Location:|'
    if re.search(pattern, text):
        split_text = re.split(pattern, text)
        address_text = split_text[-1].strip()
        return address_text[:15]
    else:
        return None
    


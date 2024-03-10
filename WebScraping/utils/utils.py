import logging
import csv
from utils.filters import verify_phone_number, verify_address, extract_phone_number_after_split, extract_address_after_split

logging.basicConfig(level=logging.INFO)

def data_entry(data, tags):
    for tag in tags:
        text = tag.get_text(strip=True)
        if text and text != "":
            if verify_phone_number(text) and not data.get('phone_data'):
                data['phone_data'] = text
            if not data.get('phone_data'): 
                data['phone_data'] = extract_phone_number_after_split(text)
            if verify_address(text) and not data.get('address_data'):
                data['address_data'] = text
            if not data.get('address_data'):
                data['address_data'] = extract_address_after_split(text)
    return data

def get_initial_urls_from_csv(file_path):
    initial_urls = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            initial_urls.append(row[0]) 
    return initial_urls

def extract_phone_number(text):
    phone_index = text.find("Phone:")
    if phone_index != -1:
        phone_text = text[phone_index + len("Phone:"):]
        return phone_text.strip()
    return None

def extract_address(text):
    address_index = text.find("Address:")
    if address_index != -1:
        address_text = text[address_index + len("Address:"):]
        return address_text.strip()
    return None

def get_links():
    links = []
    with open("WebScraping\sample-websites.csv", "r", encoding="utf8") as f:
        reader = csv.reader(f)
        next(reader)  
        for row in reader:
            links.append(row[0])
    return links  
import csv
import time
import aiohttp
import asyncio
import re
import os
from bs4 import BeautifulSoup
from utils.utils import data_entry, get_links
from utils.filters import verify_website_link
from urllib.parse import urljoin
import pandas as pd

asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

async def get_response(session, urls):
    try:
        data = {}
        data_url = ""
        for url in urls:
            data['domain'] = url
            data_url = f"https://{url}"
            async with session.get(data_url, headers=headers, timeout=30, ssl=False) as resp:
                status = resp.status
                if status != 200:
                    data_url = f"http://{url}"
                    async with session.get(data_url, headers=headers, timeout=30, ssl=False) as resp:
                        if resp.status == 200:
                            text = await resp.text(encoding='utf-8', errors='ignore')
                        else:
                            text = ""
                else:
                    text = await resp.text(encoding='utf-8', errors='ignore')
            soup = BeautifulSoup(text, 'html5lib')
            elements = {
                'contact': soup.find("a", href=re.compile(r'/contact\b')),
                'social': soup.find("a", href=re.compile(r'/social\b'))
            }
            website_data = None
            for element in elements.values():
                if element:
                    website_data = await extract_website_data(session, element, data, data_url)
                    if website_data:
                        return website_data
            if not website_data:
                elements = soup.find_all(lambda tag: tag.name != 'style')
                website_data = data_entry(data, elements)
            social_link = soup.find("a", href=re.compile(r'facebook\b'))
            data['social_href'] = social_link.get('href') if social_link else None
    
            return website_data
    except aiohttp.ClientError as e:
        print(f"Error fetching {data_url}: {e}")
        return None  
    except asyncio.TimeoutError as e:
        print(f"Timeout fetching {data_url}: {e}")
        return None  
    except Exception as e:
        print(f"Error processing {data_url}: {e}")
        return None

async def extract_website_data(session, element, data, url):
    if verify_website_link(element.get('href')):
        contact_page_link = element.get('href')
    else:
        contact_page_link = urljoin(url, element.get('href'))
    try:
        async with session.get(contact_page_link, headers=headers, timeout=30, ssl=False) as resp:
            status = resp.status
            if status == 200:
                text = await resp.text(encoding='utf-8', errors='ignore')
        contact_soup = BeautifulSoup(text, 'html5lib')
        for style in contact_soup.find_all("style"):
            style.extract()
        for script in contact_soup.find_all("script"):
            script.extract()
        elements = contact_soup.find_all()
        website_data = data_entry(data, elements)
        return website_data
    except Exception as e:
        print(f"Error extracting {element.name} data for {contact_page_link}: {e}")
        return None     
    
async def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]  
      
async def main():
    start_time = time.time()
    initial_urls = get_links()
    i = 0
    phone_counter = 0
    social_counter = 0
    address_counter = 0
    try:
        with open("scraped_data.csv", "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["domain", "phone_number", "social", "location"])
        
            async with aiohttp.ClientSession() as session:
               async for chunk in chunks(initial_urls, 100):
                   tasks = []
                   semaphore = asyncio.Semaphore(50)
                   for url in chunk:
                       async with semaphore:
                           tasks.append(asyncio.create_task(get_response(session, [url])))
                   results = await asyncio.gather(*tasks)
                   for result in results:
                       if result is not None:
                            i += 1
                            if result.get('phone_data'):
                                phone_counter += 1
                            if result.get('social_href'):
                                social_counter += 1
                            if result.get('address_data'):
                                address_counter += 1
                            writer.writerow([result.get('domain', ""),
                                            result.get('phone_data', ""),
                                            result.get('social_href', ""),
                                            result.get('address_data', "")])
                            
        df1 = pd.read_csv('WebScraping\sample-websites-company-names.csv')
        df2 = pd.read_csv('scraped_data.csv')
        combined_df = pd.merge(df1, df2, on='domain', how='inner')

        combined_df.to_csv("merged_data.csv", index=False)
    except Exception as e:  
        print(e)
    if i > 0:
        end_time = (time.time() - start_time) / 60
        print(f"{end_time:.2f} mins.")
        perc = (i * 100) / len(initial_urls)
        print(f"{perc:.2f}% of websites reached. {i} / {len(initial_urls)} sites.")
        phone_perc = (phone_counter * 100) / i
        social_perc = (social_counter * 100) / i
        address_perc = (address_counter * 100) / i
        print(f"Phone Count: {phone_perc:.2f}%")
        print(f"Social Count: {social_perc:.2f}%")
        print(f"Address Count: {address_perc:.2f}%")
    else:
        print("No websites were processed.")  

asyncio.run(main())


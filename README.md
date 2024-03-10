# Web Scraper Python 

## Prerequisites

- Python 3.x
- Libraries:
  - aiohttp
  - asyncio
  - BeautifulSoup
  - pandas

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your/repository.git
	```
## Description

	- The script fetches data such as phone numbers, social media links, and addresses from the provided list of websites. It utilizes asynchronous requests for improved performance. The data is then saved to a CSV file named - - scraped_data.csv. Additionally, it merges the scraped data with company names from another CSV file named sample-websites-company-names.csv, and saves the combined data to merged_data.csv.

## Details

	- After extracting the websites from the list, the program attempts to access the HTTPS domain of each website. If unsuccessful, it falls back to HTTP. To handle cases where data such as contact information and social links reside on specific routes (e.g., /contact, /social), the program first checks for their existence. If found, it routes the page accordingly. Otherwise, it searches the home page for relevant data.
	
	- The data fetching is using asyncio for asynchronous handling of the requests, additionally i added a timeout of 30 seconds to cancel the search if the site is not reached and a semaphore for multiple tasks handling. The list of websites is handled in chunks for efficiency and retention.

	- When searching through the site, the program verifies data using utility functions that utilize regular expressions to validate phone numbers and locations. If data is not directly found, the program performs another check, searching for keywords such as "Phone:" or "Location:" and extracting information accordingly.

	- Finally, the program increments the entries found and calculates percentages to indicate the success rate of data retrieval. It then generates a CSV file containing information from the websites, which is merged with the contents of `sample-websites-company-names.csv`.

# API for elasticsearch NodeJS

This Node.js script facilitates indexing data from a CSV file into an Elasticsearch index and searching for specific documents within that index.

## Prerequisites

- Node.js installed on your machine
- Elasticsearch instance accessible with appropriate credentials

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your/repository.git
   ```

## Description

	- The script consists of two main functions:

	    - indexData: Reads data from the CSV file specified in merged_data.csv, then indexes each row into the Elasticsearch index specified in the configuration. It handles duplicate documents by checking for existing documents before indexing.

	    - searchData: Performs a search query on the Elasticsearch index based on provided search criteria. It constructs a search query based on the fields specified in the body parameter and returns the matching document.

## Details

	- The program connects to an elasticsearch server using the credentials from the config file and creates a new index with the data from the merged csv returned by the python program. The program also checks if the domain is already added in the list. 

	- The elasticsearch data is then search using the api "/api/search" by calling the function searchData that created a new body for each entry added from the request body received by api and makes a match using regular expression for each value from the object and then the api returns the data returned by the elastic search as an object.
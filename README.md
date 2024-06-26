# Minion Grid Web-Scraper

This is a small web-scraping project created for scraping the LinkedIn profiles (for now) using a centralised controller and uses multiple agents for efficiency.

## Prerequisites

- Python 3.6 or higher
- Libraries: `requests`, `beautifulsoup4`, `selenium`, `psycopg2`

## Setup

1. Install the required Python libraries with pip:

    ```bash
    pip install requests beautifulsoup4 selenium psycopg2
    ```

## Process

> The data requirements are:
> - Name
> - Current Position
> - Skills
> - LinkedIn URL
>    ___

<br>

## Usage

Run: 
``` python
python ./parent.py
```

A data-set `data-mini.csv` is formed in `./data/` directory along with that `data.csv` is also initiated. `data-mini.csv` contains basic details like `name`, `role` and for now, most importantly, `profile_URL`. Now you may analyse the size of `data-mini.csv` and according to that engage multiple `minion.py` to download and process data faster simultaneously.

Run:
```
python ./minion.py
>>> Enter the starting index: <start_index as per your choice>
>>> Enter the ending index: <end_index as per your choice>
```

The data of all the profiles will simultaneously be appended to the `data.csv`. And further processed to postgreSQL.

<br>

## Process

1. Initially, I considered using the LinkedIn APIs available for public or developer use. However, they were either deprecated or not relevant (mostly for scraping jobs, not profiles).

2. The most relevant and straightforward method I found was to use Google search with some filters, such as:

    - The site filter "site:" as `"site:linkedin.com/in/" OR "site:linkedin.com/pub/"`
    - And since searching for profiles the intitle filter as `-intitle:"profiles`
    - The job profile as simply `"Software Developer"`
    - Email by adding `"@gmail.com" OR "@yahoo.com"` (not done here)
    - Location can also be added as a field with `Software Developer` (not done for this case).

- Final `url` used was `https://www.google.com/search?q=+"Software+Developers" -intitle:"profiles" -inurl:"dir/+"+site:linkedin.com/in/+OR+site:linkedin.com/pub/`

<br>

3. By this method, for each person, majority of the data as `name`, `profile URL`, `position` is obtained. We just need to extract the data from parsing the request by passing the URL (in which we applied filters)


4. For the fields as `Current Position`, `Past Experiences`, `Education`, `About` and other possible data is a bit tough. But I thought to get it by now parsing the individual `profile URL`, since we get it in previous step.

5. I've used `Selenium` to prevent the cached count of requested pages as it opens a completely new Chromium window each time.

<br>

> Linked prevents the multiple requests for profiles without logging in. It also hides some of the data which can be only viewed through login. Also, there are popups whose classes are needed to be found to access the page. 

<br>

6. After this, most of the processing is to be done by parsing the data recieved, finding the spans containing data using `BeautifulSoup` library.

7. In the end we get all the required data, namely, `name`, `profile URL`, `Current Position`, etc. I've also included the fields of `About`, `Past Experiences`, `Education`, which can also be potentially useful for Skills.

<br>

In the `./xtras/scraper.py` or `./parent.py` script, there are a few parameters you can change:

> `url`: This is the URL of the Google search results page. You can change the search query to scrape different LinkedIn profiles.

> `number_of_swipes`: This is the number of times the script will scroll down on the Google search results page to load more results. You can increase this number to scrape more profiles.

The comments in the code explain the process during the extraction. postgreSQL (.sql) file will be included in the data and the images are self explanatory.

> The `Past Experience` field is not in the current `data.csv` but is implemented later into the `./xtras/scrapper.py` and `./minion.py`. The re-run for the entire data was time consuming and also the IP-address was restricted to request the data. The re-run of `./parent.py` and `./minion.py` will populate that field too.

> Thanks..!!

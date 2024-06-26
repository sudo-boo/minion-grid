from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import unquote
import time

# Gathering data from Google search results using Selenium
# The goal is to get the names, roles, URLs of the LinkedIn profiles of Software Developers

# The search query is: "Software Developers" -intitle:"profiles" -inurl:"dir /" site:linkedin.com/in/ OR site:linkedin.com/pub/
# ------------------------------------------------------------------------------------------------------------------

url = "https://www.google.com/search?q=+%22Software+Developers%22 -intitle:%22profiles%22 -inurl:%22dir/+%22+site:linkedin.com/in/+OR+site:linkedin.com/pub/"
number_of_swipes = 50

# ------------------------------------------------------------------------------------------------

def extract_name_and_role(html):
    soup = BeautifulSoup(html, 'html.parser')
    span_tags = soup.find_all('span', {'jscontroller': 'msmzHf'})

    urls = []
    names = []
    roles = []

    for span in span_tags:
        a = span.find('a', {'jsname': 'UWckNb'})
        if a:
            ping = a.get('ping')
            if ping:
                parts = ping.split('&')
                for part in parts:
                    if part.startswith('url=') and "linkedin" in part:
                        url = part[4:]
                        url = unquote(url)
                        print(url)
                        urls.append(url)
                        h3 = span.find('h3')
                        if h3:
                            text = h3.text
                            text = text.replace('...','')
                            text = text.replace(',','')
                            parts = text.split(' - ')
                            if len(parts) > 1:
                                name = parts[0]
                                role = parts[1]
                            else:
                                name = text
                                role = 'Role not found'
                            names.append(name)
                            roles.append(role)
    return urls, names, roles

# ------------------------------------------------------------------------------------------------------------------
# Gathering data from Google search results using Selenium
    
def gather_data_from_google_search():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    # There might be a small verification required to prove that you are not a robot. You may need to pass it manually, thats why adding a sleep here.
    time.sleep(15)

    for _ in range(number_of_swipes):

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # wait for the "More results" button to be present, and then click it
        try:
            more_results = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "RVQdVd")))
            more_results.click()

        except Exception as e:
            print("More results button not found")

    html = driver.page_source

    driver.quit()

    # # save the source code to a file
    # # -------for debug purposes-------
    # with open('search-result.html', 'w', encoding='utf-8') as f2:
    #     f2.write(html)

    return html


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Processing the HTML to extract the data
# Some patterns were observed in the HTML that can be used to extract the data which are described in functions

def main():
    
    html = gather_data_from_google_search()
    # urls = extract_name_and_role(html)
    urls, names, roles = extract_name_and_role(html)

    with open('./data/data-mini.csv', 'w', encoding='utf-8') as file:
        # file.write('Name,URL,Role\n')
        for i in range(len(urls)):
            file.write(f'{names[i]},{urls[i]},{roles[i]}\n')
    # # print(urls)
        
    with open('./data/data.csv', 'w', encoding='utf-8') as file:
        file.write('Name,URL,Role,Current Workplace,Past Experience,Education,About\n')

    print('Data extraction complete. Check data.csv for the results.')

if __name__ == "__main__":
    main()
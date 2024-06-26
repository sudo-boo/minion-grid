from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import unquote
import time
import random
import csv

# Gathering data from Google search results using Selenium
# The goal is to get the names, roles, URLs of the LinkedIn profiles of Software Developers

# The search query is: "Software Developers" -intitle:"profiles" -inurl:"dir /" site:linkedin.com/in/ OR site:linkedin.com/pub/
# ------------------------------------------------------------------------------------------------------------------

def write_data_to_csv(name, url, role, education_data, about_data, current_workplace_data, past_experience_data):
    with open('./data/data.csv', 'a', encoding='utf-8') as file:
        file.write(f'"{name}", "{url}", "{role}", "{current_workplace_data}", "{past_experience_data}", "{education_data}", "{about_data}"\n')

# ------------------------------------------------------------------------------------------------

def extract_education_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    education_section = soup.find('section', {'data-section': 'educationsDetails'})
    if not education_section:
        return ''

    education_list = education_section.find('ul', {'class': 'education__list'})
    if not education_list:
        return ''

    education_data = []
    for li in education_list.find_all('li', {'class': 'profile-section-card'}):
        institute_name = li.find('h3').text.strip()
        institute_name = institute_name.replace('\n', ' ')
        degree = li.find('h4').text.strip()
        degree = degree.replace('\n', ' ')
        education_data.append(f'institute_name: {institute_name} - degree: {degree}')

    return '; '.join(education_data)

# ------------------------------------------------------------------------------------------------

def extract_about_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    about_section = soup.find('section', {'data-section': 'summary'})
    if not about_section:
        return ''

    about_content = about_section.find('div', {'class': 'core-section-container__content'})
    if not about_content:
        return ''

    about_text = about_content.get_text(separator=' ', strip=True)
    return about_text

# ------------------------------------------------------------------------------------------------

def extract_current_workplace_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    current_workplace_section = soup.find('div', {'data-section': 'currentPositionsDetails'})
    if not current_workplace_section:
        return 'No current position details found'

    current_workplace_div = current_workplace_section.find('div', {'data-test-id': 'top-card-link'})
    current_workplace_link = current_workplace_section.find('a', {'data-test-id': 'top-card-link'})

    if current_workplace_div:
        current_workplace_text = current_workplace_div.get_text(separator=' ', strip=True)
    elif current_workplace_link:
        current_workplace_text = current_workplace_link.get_text(separator=' ', strip=True)
    else:
        return 'No current position details found'

    return current_workplace_text

# ------------------------------------------------------------------------------------------------

def extract_experience_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    experience_section = soup.find('section', {'data-section': 'experience'})
    if not experience_section:
        return 'No experience details found'

    experience_list = experience_section.find('ul', {'class': 'experience__list'})
    if not experience_list:
        return 'No experience details found'

    experience_data = []
    for li in experience_list.find_all('li', {'class': 'profile-section-card'}):
        company_name = li.find('h3').text.strip()
        company_name = company_name.replace('\n', ' ')
        job_title = li.find('h4').text.strip()
        job_title = job_title.replace('\n', ' ')
        duration = li.find('span', {'class': 'date-range'}).text.strip()
        duration = duration.replace('\n', ' ')
        duration = duration.replace('\t', ' ')
        experience_data.append(f'Worked at: {company_name} - Job Title: {job_title} - Duration: {duration}')

    return '; '.join(experience_data)

# ------------------------------------------------------------------------------------------------

def get_profile_pages(name, url, role):
    try:
        driver = webdriver.Chrome()
        driver.get(url)

        # A modal appears when opened the website. Wait for it to appear and then close it
        wait = WebDriverWait(driver, 4)
        modal_close_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-tracking-control-name="public_profile_contextual-sign-in-modal_modal_dismiss"]')))

        modal_close_button.click()

        # Save the page
        html = driver.page_source
        driver.quit()

        # if not os.path.exists('./html'):
        #     os.makedirs('./html')
        # with open(f'./html/{name}.html', 'w', encoding='utf-8') as file:
        #     file.write(html)

        education_data = extract_education_data(html)
        about_data = extract_about_data(html)
        current_workplace_data = extract_current_workplace_data(html)
        past_experience_data = extract_experience_data(html)
        write_data_to_csv(name, url, role, education_data, about_data, current_workplace_data, past_experience_data)
    except Exception as e:
        print(f"An error occurred while processing the URL {url}: {str(e)}")


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Processing the HTML to extract the data
# Some patterns were observed in the HTML that can be used to extract the data which are described in functions


def main():
    with open('./data/data-mini.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    start = int(input('Enter the starting index: '))
    end = int(input('Enter the ending index: '))
    lines = lines[start:end]
    counter = 0

    for line in lines:
        name, url, role = line.strip().split(',')
        url = url.strip()  # Strip leading/trailing white spaces
        # print(url)
        print (f'>>>> Processing index : {start + counter} ({counter} / {len(lines)}): -----------------')
        get_profile_pages(name, url, role)
        counter += 1

    print(f'Data extraction completed for index {start} to {end}. Check data.csv for the results.')

if __name__ == "__main__":
    main()
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import unquote
import time
import random

# Gathering data from Google search results using Selenium
# The goal is to get the names, roles, URLs of the LinkedIn profiles of Software Developers

# The search query is: "Software Developers" -intitle:"profiles" -inurl:"dir /" site:linkedin.com/in/ OR site:linkedin.com/pub/
# ------------------------------------------------------------------------------------------------------------------

url = "https://www.google.com/search?q=+%22Software+Developers%22 -intitle:%22profiles%22 -inurl:%22dir/+%22+site:linkedin.com/in/+OR+site:linkedin.com/pub/"
number_of_swipes = 20

# ------------------------------------------------------------------------------------------------

def write_data_to_csv(name, url, role, education_data, about_data, current_workplace_data):
    with open('./data/data.csv', 'a', encoding='utf-8') as file:
        file.write(f'"{name}", "{url}", "{role}", "{current_workplace_data}", "{education_data}", "{about_data}"\n')

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

def extract_name_and_role(text):
    text = text.replace('...','')
    text = text.replace(',','')
    parts = text.split(' - ')
    if len(parts) > 1:
        # remove , from parts
        name = parts[0]
        role = parts[1]
    else:
        name = text
        role = 'Role not found'
    return name, role

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

def get_profile_pages(text, url):
    try:

        driver = webdriver.Chrome()
        driver.get(url)

        # A modal appears when opened the website. Wait for it to appear and then close it
        wait = WebDriverWait(driver, 20)
        modal_close_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-tracking-control-name="public_profile_contextual-sign-in-modal_modal_dismiss"]')))
        
        time.sleep(random.randint(1, 3))
        modal_close_button.click()

        # Sleep for 20 seconds
        time.sleep(random.randint(5, 10))

        # Save the page
        html = driver.page_source
        driver.quit()

        time.sleep(3)

        # --------for debug purposes--------
        # with open(f"ji{i}.html", "w", encoding='utf-8') as f:
        #     f.write(html)
        #     f.close()
        
        # --------for debug purposes--------
        # with open(f"ji{i}.html", "r", encoding='utf-8') as f:
        #     html = f.read()
        #     f.close()
        
        education_data = extract_education_data(html)
        # print(education_data)
        about_data = extract_about_data(html)
        # print(about_data)
        current_workplace_data = extract_current_workplace_data(html)
        # print(current_workplace_data)
        name, role = extract_name_and_role(text)
        write_data_to_csv(name, url, role, education_data, about_data, current_workplace_data)
    except Exception as e:
        print(e)
        print(f"Error for {url}")

# ------------------------------------------------------------------------------------------------------------------
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

def analyse(html):
    soup = BeautifulSoup(html, 'html.parser')

    # observed that the URLs are in the 'ping' attribute of the <a> tag within the <span> tag with the 'jsname' attribute set to 'UWckNb'
    span_tags = soup.find_all('span', {'jscontroller': 'msmzHf'})

    for span in span_tags:
        a = span.find('a', {'jsname': 'UWckNb'})
        if a:
            ping = a.get('ping')
            if ping:
                parts = ping.split('&')
                for part in parts:
                    # if the part starts with 'url=' and contains 'linkedin', extract the URL
                    if part.startswith('url=') and "linkedin" in part:
                        url = part[4:]
                        url = unquote(url)
                        # find the <h3> tag within the <span> tag and extract the name
                        h3 = span.find('h3')
                        if h3:
                            # observation that 'name', 'role' and 'working at' was split by ' - ' and the name was the first part
                            text = h3.text
                            # save it in a list and if list size if >=2 then only add name and role to the file
                            
                        # export the text and url to a file
                        print(text)
                        
                        get_profile_pages(text, url)

def main():
    
    with open('./data/data.csv', 'w', encoding='utf-8') as file:
        file.write('Name,URL,Role,Current Workplace,Education, About\n')
    html = gather_data_from_google_search()
    analyse(html)

    print('Data extraction complete. Check data.csv for the results.')

if __name__ == "__main__":
    main()
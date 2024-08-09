from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

driver = webdriver.Chrome()

driver.get('https://www.indeed.com/companies/best-companies')
driver.maximize_window()

# Creating a dictionary to store the scraped data
data = {
    'Company Name': [],
    'Reviews': [],
    'Total Reviews': [],
    'Company Type': [],
    'Employees Estimation': [],
    'Company Description': []
}

try:
    for i in range(1, 150):
        # Wait until the data is loaded
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'h2')))
        
        # Scrape data
        company_names = driver.find_elements(By.TAG_NAME, 'h2')
        reviews = driver.find_elements(By.CLASS_NAME, 'css-1qqp5xo.e1wnkr790')
        total_reviews = driver.find_elements(By.CLASS_NAME, 'css-1kxybv0.e19afand0')
        company_types = driver.find_elements(By.CLASS_NAME, 'css-j3kgaw.e1wnkr790')
        company_descriptions = driver.find_elements(By.CLASS_NAME, 'css-1io73yq.eu4oa1w0')

        # Storeing the data in the dictionary
        for name, review, total_review, company_type, description in zip(company_names, reviews, total_reviews, company_types, company_descriptions):
            data['Company Name'].append(name.text)
            data['Reviews'].append(review.text)
            data['Total Reviews'].append(total_review.text)
            
            # Split company_type
            split_types = company_type.text.split(' - ')
            if len(split_types) > 1:
                data['Company Type'].append(split_types[0])
                data['Employees Estimation'].append(split_types[1])
            else:
                data['Company Type'].append(split_types[0])
                data['Employees Estimation'].append('N/A')
            
            data['Company Description'].append(description.text)

        # Find and click the button with a specific title attribute
        try:
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[title="Next"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(5)
        except Exception as e:
            print(f"Button click failed: {e}")
            break

finally:
    driver.quit()

# Writing the dictionary data to a CSV file
csv_file = 'companies_data.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(data.keys())
    rows = zip(*data.values())
    writer.writerows(rows)

print(f"Data has been written to {csv_file}")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

driver = webdriver.Chrome()

driver.get('https://www.indeed.com/companies/best-companies')
driver.maximize_window()

data = {
    'Company Name': [],
    'Reviews': [],
    'Total Reviews': [],
    'Company Description': []
}

try:
    for i in range(1, 10):
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'h2')))
        
        company_names = driver.find_elements(By.TAG_NAME, 'h2')
        reviews = driver.find_elements(By.CLASS_NAME, 'css-1qqp5xo.e1wnkr790')
        total_reviews = driver.find_elements(By.CLASS_NAME, 'css-1kxybv0.e19afand0')
        company_descriptions = driver.find_elements(By.CLASS_NAME, 'css-1io73yq.eu4oa1w0')

        for name, review, total_review, description in zip(company_names, reviews, total_reviews, company_descriptions):
            data['Company Name'].append(name.text)
            data['Reviews'].append(review.text)
            data['Total Reviews'].append(total_review.text)
            data['Company Description'].append(description.text)
            
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[title="Next"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            driver.execute_script("arguments[0].click();", button)
            
            WebDriverWait(driver, 10).until(EC.staleness_of(button))
            time.sleep(5)
            
        except Exception as e:
            print(f"Button click failed: {e}")
            break

finally:
    driver.quit()

csv_file = 'companies_data.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(data.keys())
    rows = zip(*data.values())
    writer.writerows(rows)

print(f"Data has been written to {csv_file}")

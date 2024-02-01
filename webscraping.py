import csv
import time
import os
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Set the News Category to Scrape
news_q_category = ["Business", "Entertainment", "Technology", "Science", "Health"]

def scrape_cnn_data():
    driver = webdriver.Chrome(options=options)
    print('Start Scraping CNN')
    all_cnn_data = []
    total_pages = 1
    
    for query in news_q_category:
        page_count = 1
        url = generate_search_url('CNN', query, page_count)
        
        print(f"Scraping Category: {query}")
        
        driver.get(url)

        for page in range(1, total_pages + 1):
            print(f"Scraping Page {page}")
            
            titles = None
            
            # Retry loop to handle StaleElementReferenceException
            for _ in range(3):  # Retry 3 times
                try:
                    titles = driver.find_elements(By.XPATH, "//span[@class='container__headline-text']")
                    break  # Break the retry loop if successful
                except StaleElementReferenceException:
                    print("StaleElementReferenceException occurred. Refreshing the elements...")
                    time.sleep(2)  # Wait before retrying
                    continue  # Retry
            
            if titles is None:
                print("Failed to retrieve titles after retries. Exiting page scrape.")
                break
            category = query.lower()

            if category == 'business':
                category = 'b'
            elif category == 'entertainment':
                category = 'e'
            elif category == 'technology' or 'science':
                category = 't'
            elif category == 'health':
                category = 'm'
            
            scraped_data = []
            for title in titles:
                scraped_data.append({
                    'TITLE': title.text,
                    'CATEGORY': category
                })
            
            all_cnn_data.extend(scraped_data)

            # Navigate to next page
            try:
                next_button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='pagination-arrow pagination-arrow-right search__pagination-link text-active']"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                next_button.click()
                print(f"Next Page")
                page_count += 1

                time.sleep(3)
            except Exception as e:
                print(f"No more pages")
                break  # Break the loop if unable to find the next button
            
    driver.close()
    print("Finished CNN")
    return save_to_csv(all_cnn_data, 'CNN1_dataset.csv')
    
def scrape_bbc_data():
    driver = webdriver.Chrome(options=options)
    print('Start Scraping BBC')
    total_pages = 50
    all_bbc_data = []
    
    for query in news_q_category:
        page_count = 1
        url = generate_search_url('BBC', query, page_count)
        print(f"Scraping Category: {query}")
        driver.get(url)
        
        for page in range(1, total_pages + 1):
            print(f"Scraping Page {page}")
            
            titles = driver.find_elements(By.XPATH, "//a[@class='ssrcss-its5xf-PromoLink exn3ah91']")
            category = query.lower()

            if category == 'business':
                category = 'b'
            elif category == 'entertainment':
                category = 'e'
            elif category == 'technology' or 'science':
                category = 't'
            elif category == 'health':
                category = 'm'
            
            scraped_data = []
            for title in titles:
                scraped_data.append({
                    'TITLE': title.text,
                    'CATEGORY': category
                })
            
            all_bbc_data.extend(scraped_data)

            # Navigate to next page
            try:
                next_button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='main-content']/div[5]/div/div/nav/div/div/div[4]"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                next_button.click()
                print(f"Next Page")
                page_count += 1

                time.sleep(3)
            except Exception as e:
                print(f"No more pages")
                break  # Break the loop if unable to find the next button
    
    driver.close()
    print("Finished BBC")
    return save_to_csv(all_bbc_data, 'BBC_dataset.csv')

def scrape_apnews_data():
    driver = webdriver.Chrome(options=options)
    print('Start Scraping APNEWS')
    total_pages = 50
    all_apnews_data = []
    
    for query in news_q_category:
        page_count = 1
        print(f"Scraping Category: {query}")
    
        for page in range(1, total_pages + 1):
            print(f"Scraping Page {page}")
            
            url = generate_search_url('APNEWS', query, page_count)
            driver.get(url)
            
            titles = driver.find_elements(By.XPATH, "//span[@class='PagePromoContentIcons-text']")
            category = query.lower()

            if category == 'business':
                category = 'b'
            elif category == 'entertainment':
                category = 'e'
            elif category == 'technology' or 'science':
                category = 't'
            elif category == 'health':
                category = 'm'
            
            scraped_data = []
            for title in titles:
                scraped_data.append({
                    'TITLE': title.text,
                    'CATEGORY': category
                })
            
            all_apnews_data.extend(scraped_data)
            
            # Increment page_count for the next iteration
            print('Next Page')
            page_count += 1

            time.sleep(3)  # Adjust this sleep duration as needed
    
    driver.close()
    print("Finished APNEWS")
    return save_to_csv(all_apnews_data, 'APNEWS_dataset.csv')

   
def scrape_abcnews_data():
    driver = webdriver.Chrome(options=options)
    print('Start Scraping ABCNEWS')
    total_pages = 150
    all_abcnews_data = []

    
    for query in news_q_category:
        page_count = 1
        url = generate_search_url('ABCNEWS', query, page_count)
        print(f"Scraping Category: {query}")
    
        driver.get(url)
        
        for page in range(1, total_pages + 1):
            print(f"Scraping Page {page}")
            
            # titles = driver.find_elements(By.XPATH, "//span[@class='container__headline-text']")
            titles = None
            
            # Retry loop to handle StaleElementReferenceException
            for _ in range(3):  # Retry 3 times
                try:
                    titles = driver.find_elements(By.XPATH, "//div[@class='ContentRoll__Headline']/h2/a[@class='AnchorLink']")
                    break  # Break the retry loop if successful
                except StaleElementReferenceException:
                    print("StaleElementReferenceException occurred. Refreshing the elements...")
                    time.sleep(2)  # Wait before retrying
                    continue  # Retry
            
            if titles is None:
                print("Failed to retrieve titles after retries. Exiting page scrape.")
                break
            category = query.lower()

            if category == 'business':
                category = 'b'
            elif category == 'entertainment':
                category = 'e'
            elif category == 'technology' or 'science':
                category = 't'
            elif category == 'health':
                category = 'm'
            
            scraped_data = []
            for title in titles:
                scraped_data.append({
                    'TITLE': title.text,
                    'CATEGORY': category
                })
            
            all_abcnews_data.extend(scraped_data)

            # Navigate to next page
            try:
                next_button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='fitt-analytics']/div/main/div[2]/section[1]/div/div[4]/a[2]"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                next_button.click()
                print(f"Next Page")
                page_count += 1
                time.sleep(3)
            except Exception as e:
                print(f"No more pages")
                break  # Break the loop if unable to find the next button
    
    driver.close()
    print("Finished ABCNEWS")
    return save_to_csv(all_abcnews_data, 'ABCNEWS_dataset.csv')

def generate_search_url(news_source, query, page):
    base_url = ""
    params = {}

    if news_source.lower() == 'cnn':
        base_url = "https://edition.cnn.com/search"
        params = {
            'q': query,
            'from': '0',
            'size': '30',
            'page': page,
            'sort': 'newest',
            'types': 'all',
            'section': '',
        }
    elif news_source.lower() == 'bbc':
        base_url = "https://www.bbc.co.uk/search"
        params = {
            'q': query,
            'd': 'news_gnl',
            'seqId': '63f76c50-ad81-11ee-93be-177d84e088a8',
            'page': page,
        }
    elif news_source.lower() == 'apnews':
        base_url = "https://apnews.com/search"
        params = {
            'q': query,
            'p': page,
        }
    elif news_source.lower() == 'abcnews':
        base_url = "https://abcnews.go.com/search"
        params = {
            'searchtext': query,
            'p': page,
        }
    else:
        return None  # Return None for unsupported news sources

    # Constructing the URL with parameters
    search_url = f"{base_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    return search_url


def save_to_csv(news_data, file_name):
    folder_path = 'dataset/'
    file_path = os.path.join(folder_path)

    with open(file_name, "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["TITLE", "CATEGORY"])
        for data in news_data:
            writer.writerow([data['TITLE'], data['CATEGORY']])

    print(f"Saved data to: {file_path}")
 
    
def combined_csv_data():
    # replace with your folder's path
    folder_path = "dataset/"

    all_files = os.listdir(folder_path)

    # Filter out non-CSV files
    csv_files = [f for f in all_files if f.endswith('.csv')]

    # Create a list to hold the dataframes
    df_list = []

    for csv in csv_files:
        file_path = os.path.join(folder_path, csv)
        try:
            # Try reading the file using default UTF-8 encoding
            df = pd.read_csv(file_path)
            df_list.append(df)
        except UnicodeDecodeError:
            try:
                # If UTF-8 fails, try reading the file using UTF-16 encoding with tab separator
                df = pd.read_csv(file_path, sep='\t', encoding='utf-16')
                df_list.append(df)
            except Exception as e:
                print(f"Could not read file {csv} because of error: {e}")
        except Exception as e:
            print(f"Could not read file {csv} because of error: {e}")

    # Concatenate all data into one DataFrame
    combined_df = pd.concat(df_list, ignore_index=True)

    # Save the final result to a new CSV file
    return combined_df.to_csv(os.path.join(folder_path, 'combined_test_dataset.csv'), index=False)

def clean_data():
    data = pd.read_csv('dataset/combined_test_dataset.csv')

    data['TITLE'] = data['TITLE'].apply(clean_text)

    data = data.dropna(subset=['TITLE'])  # Drop rows with NaN values in 'TITLE' column

    # Save the cleaned data back to a CSV file
    return data.to_csv('test_dataset.csv', index=False)

def clean_text(text):
    if pd.isnull(text) or text == np.nan:  # Check for NaN values or string "NaN"
        return ""  # Replace NaN with empty string
    clean_text = text.encode('latin1', 'ignore').decode('utf-8', 'ignore')
    return clean_text


scrape_cnn_data()
time.sleep(5)
scrape_bbc_data()
time.sleep(5)
scrape_apnews_data()
time.sleep(5)
scrape_abcnews_data()
time.sleep(5)
combined_csv_data()
time.sleep(5)
clean_data()


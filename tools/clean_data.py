import pandas as pd
import numpy as np  # Import NumPy for NaN handling

def clean_data():
    data = pd.read_csv('webscrape_data/combined_test_dataset.csv')

    data['TITLE'] = data['TITLE'].apply(clean_text)

    data = data.dropna(subset=['TITLE'])  # Drop rows with NaN values in 'TITLE' column

    # Save the cleaned data back to a CSV file
    return data.to_csv('webscrape_data/cleaned_test_dataset.csv', index=False)

def clean_text(text):
    if pd.isnull(text) or text == np.nan:  # Check for NaN values or string "NaN"
        return ""  # Replace NaN with empty string
    clean_text = text.encode('latin1', 'ignore').decode('utf-8', 'ignore')
    return clean_text

clean_data()

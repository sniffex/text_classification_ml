import pandas as pd
import os

# Disabling warnings:
import warnings 
warnings.filterwarnings('ignore')

# Load train data
data_path = os.path.join(os.path.dirname(__file__), 'training_dataset/newsCorpora.csv')
col_names = ["ID", "TITLE", "URL", "PUBLISHER", "CATEGORY", "STORY", "HOSTNAME", "TIMESTAMP"]
dataset = pd.read_csv(data_path, delimiter='\t', encoding='utf-8', names=col_names)

# Prepare data for training ONLY using Title and Category
training_dataset = dataset[['TITLE', 'CATEGORY']]
training_dataset.to_csv('training_dataset/training_data.csv', index=False)
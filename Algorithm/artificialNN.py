import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfVectorizer  
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Disabling warnings:
import warnings 
warnings.filterwarnings('ignore')

# Load train data
data_path = os.path.join(os.path.dirname(__file__), 'training_dataset/training_data.csv')
col_names = ['TITLE', 'CATEGORY']
training_dataset_df = pd.read_csv(data_path, encoding='utf-8', names=col_names)

X = training_dataset_df["TITLE"]
Y = training_dataset_df["CATEGORY"]
# x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
x_train = X
y_train = Y

# Prepare test data
test_data_path = os.path.join(os.path.dirname(__file__), 'webscrape_data/cleaned_test_dataset.csv')
testing_dataset = pd.read_csv(test_data_path, encoding='utf-8', names=["TITLE", "CATEGORY"])

# Filter out rows where the category is 'Category'
testing_dataset = testing_dataset[testing_dataset['CATEGORY'] != 'CATEGORY']

x_test = testing_dataset["TITLE"].fillna('')
y_test = testing_dataset["CATEGORY"]

# Encode the target labels
le = LabelEncoder()
y_train_encoded = le.fit_transform(y_train)
y_test_encoded = le.transform(y_test)

# TF-IDF vectorization for text data
tfidf = TfidfVectorizer()   
x_train_tfidf = tfidf.fit_transform(x_train)
x_test_tfidf = tfidf.transform(x_test)

# Train model using Gaussian Naive Bayes on the TF-IDF transformed data
MLPclf = MLPClassifier(
    hidden_layer_sizes=(10, 10, 10, 10, 10),
    max_iter=50,
    solver='adam',
    learning_rate_init=0.2)

MLPclf = MLPclf.fit(x_train_tfidf, y_train_encoded)

# Make predictions on the test set
y_pred = MLPclf.predict(x_test_tfidf)

# Model Evaluation
print(classification_report(y_test_encoded, y_pred))


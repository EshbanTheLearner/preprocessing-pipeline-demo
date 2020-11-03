import pandas as pd
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from  nltk.stem import SnowballStemmer
import os

path = os.environ["S3_DATA_PATH"]

print(f"\nInside Python Script\nPath = {path}\n")
print(f"Loading Data\n")

df = pd.read_csv(path, encoding="ISO-8859-1", names=["label", "id", "date", "flag", "user", "tweet"])
print(f"Data has {df.shape[0]} rows and {df.shape[1]} columns\n")

TEXT_CLEANING_RE = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"

stop_words = stopwords.words("english")
stemmer = SnowballStemmer("english")

def preprocess(text, stem=False):
    # Remove link, user and special characters
    text = re.sub(TEXT_CLEANING_RE, ' ', str(text).lower()).strip()
    tokens = []
    for token in text.split():
        if token not in stop_words:
            if stem:
                tokens.append(stemmer.stem(token))
            else:
                tokens.append(token)
    return " ".join(tokens)
print(f"Starting cleaning process")
df.text = df.text.apply(lambda x: preprocess(x))
print("Data cleaning completed, saving to CSV!\n")

df.to_csv("twitter_data_cleaned.csv", index=False)
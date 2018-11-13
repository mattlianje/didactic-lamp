# Load the Pandas libraries with alias 'pd'
import pandas as pd
import re
from collections import Counter
import nltk
#nltk.download()

# Read data from file 'filename.csv'
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later)
data = pd.read_csv("fake-cleaned.csv")

#Loop through article titles and concatenate into one big string
article_text = ""
for i in range(0, 50):
    current_text = str(data.at[i, 'text']) #Define the column here
    article_text = article_text + " " + current_text

words = re.findall(r'\w+', article_text) #This finds words in the document
cap_words = [word.lower() for word in words] #capitalizes all the words

#Remove boring words
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
cap_words = [w for w in cap_words if not w in stop_words]

word_counts = Counter(cap_words) #counts the number each time a word appears

print(word_counts)
most_common,num_most_common = Counter(word_counts).most_common(1)[0]

top_words = word_counts[0:5]
for i in top_words:
    print(top_words[i])

#print(data.at[0, 'thread_title'])
#article_title = data.at[0, 'thread_title']
#print(article_title)
#words = re.findall(r'\w+', article_title) #This finds words in the document

#print("Times 100percentfedup appears: ", len(data[data['site_url'] == '100percentfedup.com']))
#print("Times 100 appears: ", len(data[data['site_url'].str.contains("100")]))
#print("Times muslim appears: ", len(data.loc[data.thread_title.str.contains("Muslim", na=False)]))



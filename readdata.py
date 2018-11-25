# Load the Pandas libraries with alias 'pd'
import pandas as pd
import re
import numpy as np
from collections import Counter
import nltk
#nltk.download()

# Read data from file 'filename.csv'
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later)
data = pd.read_csv("fake-cleaned.csv")

#Loop through article titles and concatenate into one big string
row_words = []
row_1 = []
for i in range(0, len(data.index)):
    article_text = str(data.at[i, 'text']) #Define the column here

    words = re.findall(r'\w+', article_text) #This finds words in the document
    low_words = [word.lower() for word in words] #All the words lowercase

    #Remove boring words
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    low_words = [w for w in low_words if not w in stop_words]

    words_array = list(set(low_words))

    from nltk.stem.porter import PorterStemmer
    porter = PorterStemmer()
    stemmed = [porter.stem(word) for word in words_array]

    #Separate words into array and print to CSV
    words_array = stemmed

    words_array = list(set(stemmed))

    #Counts the number each time a word appears
    word_counts = Counter(words_array)
    # print(word_counts)
    # most_common,num_most_common = Counter(word_counts).most_common(1)[0]
    # print(most_common)
    # print(num_most_common)

    #Print and Create vector of popular words
    if article_text == '':
        keys = np.nan
    else:
        keys = np.array(list(word_counts.keys()))
    #print(keys)
    row_words.append(keys)

for sublist in row_words:
    for item in sublist:
        row_1.append(item)
row_1 = list(set(row_1))

#row_words.insert(0, row_1)
#df_list = row_1.append(row_words)
print(row_words[:4])
#df = pd.DataFrame(df_list)
df = pd.DataFrame(row_words)
print(df)
print(len(df.index))
df.dropna(subset=[0], inplace=True)
print("New:")
print(len(df.index))
# pd.concat([pd.DataFrame(row_1), df], ignore_index=True)
r1df = pd.DataFrame(row_1)
df.to_csv("apriori_setup_text.csv")
r1df.to_csv("temp.csv")
# Create Apriori DataFrame
#for key in keys50:
#    for


#print(data.at[0, 'thread_title'])
#article_title = data.at[0, 'thread_title']
#print(article_title)
#words = re.findall(r'\w+', article_title) #This finds words in the document

#print("Times 100percentfedup appears: ", len(data[data['site_url'] == '100percentfedup.com']))
#print("Times 100 appears: ", len(data[data['site_url'].str.contains("100")]))
#print("Times muslim appears: ", len(data.loc[data.thread_title.str.contains("Muslim", na=False)]))



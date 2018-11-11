# Load the Pandas libraries with alias 'pd'
import pandas as pd
# Read data from file 'filename.csv'
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later)
data = pd.read_csv("fake-cleaned.csv")
# Preview the first 5 lines of the loaded data
data.head()
print(data.head())
print("Times 100percentfedup appears: ", len(data[data['site_url'] == '100percentfedup.com']))
print("Times 100 appears: ", len(data[data['site_url'].str.contains("100")]))
print("Times muslim appears: ", len(data.loc[data.thread_title.str.contains("Muslim", na=False)]))

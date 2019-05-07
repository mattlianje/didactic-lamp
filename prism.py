# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import requests
import tweepy
from textblob import TextBlob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from rake_nltk import Rake
from statistics import mean
from fractions import Fraction
r = Rake()

# Initialization of Twitter APIs
consumer_key = 'ueAdq7eQ5fOj3K1Ev8vdjh9KL'
consumer_secret = 'PKyfaVVPVzNlYtltqC5tDzntzq2PR22Tga1F8S9RCBVerKHSlS'

access_token = '166724523-s1l3OC589hHI3k4rLpsy12dRNK7j8F4g5c7CJdlt'
access_token_secret = 'YkqC9CrsEbRyz2ExggUHXu9WJckzsxDnvAGSQJUltxTzX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
#public_tweets = api.search('Trump')

#search_hashtag = tweepy.Cursor(api.search, q='Hillary').items(50)

#for tweet in search_hashtag:
#    print(tweet.text)

# Start seeing how to web scrape
data = pd.read_csv("fake.csv")
data2 = pd.read_csv("fakeAndReal.csv")
data2Dump = pd.DataFrame(data2)
data2Clean = data2Dump.drop(data2Dump.columns[[0]], axis=1)
data2CleanCut = data2Clean.truncate(after=5)

# Create a scores vector with a polarity score for each article title
sentimentPolarityTags = []
sentimentSubjectivityTags = []
spicinessTags = []
#spicinessScoreList = []

for index, row in data2CleanCut.iterrows():
    res = TextBlob(row['title'])
    #create three tags for polarity [-1:1] (bad, neutral, good) and three for subjectivity (neutral, medium, strong) [0:1]
    currentPolarity = res.sentiment.polarity
    currentSubjectivity = res.sentiment.subjectivity
    if currentPolarity < -0.25:
        sentimentPolarityTags.append("bad")
    if -0.25 <= currentPolarity <= 0.25:
        sentimentPolarityTags.append("neutral")
    if currentPolarity > 0.25:
        sentimentPolarityTags.append("good")

    if 0 <= currentSubjectivity <= 0.2:
        sentimentSubjectivityTags.append("neutral")
    if 0.2 < currentSubjectivity <= 0.6:
        sentimentSubjectivityTags.append("medium")
    if 0.6 < currentSubjectivity <= 1.0:
        sentimentSubjectivityTags.append("strong")

    # for each article grab the twitter hotness of the terms
    keywords = r.extract_keywords_from_text(row['title'])
    keywordList = r.get_ranked_phrases()
    # We are only taking the first 5 most key words so as not to choke the twitter api with too many requests
    del keywordList[5:]
    # --- comment this line back in ---
    print(keywordList)

    #Twitter hotness calculation
    #For each keyword get the top 5 tweets
    #spicinessTags = []
    spicinessScoreList = []
    for keyword in keywordList:
        # play with the .items(1) number to change how many tweets we want to grab to calculate the spiciness of each term
        search_hashtag = tweepy.Cursor(api.search, q=keyword).items(1)

        currentListSubjScores = []
        for tweet in search_hashtag:
            # get the subjectivity of the tweet
                #print(tweet.text)
            res2 = TextBlob(tweet.text)
            currentTweetScore = res2.sentiment.subjectivity
            currentListSubjScores.append(currentTweetScore)
        if len(currentListSubjScores) == 0:
            currentArticleSpice = 0
        if len(currentListSubjScores) > 0:
            currentArticleSpice = mean(currentListSubjScores)

        currentListSubjScores.append(0.5)

        #print(currentArticleSpice)
        spicinessScoreList.append(currentArticleSpice)
    print(spicinessScoreList)
    articleSpiciness = mean(spicinessScoreList)
    print(articleSpiciness)

    if articleSpiciness < 0.25:
        spicinessTags.append("light")
    elif 0.25 <= articleSpiciness < 0.5:
        spicinessTags.append("spicy")
    elif articleSpiciness >= 0.5:
        spicinessTags.append("jalapeno")
#
    #print(spicinessTags)
data2CleanCut['polarityTags'] = sentimentPolarityTags
data2CleanCut['subjectivityTags'] = sentimentSubjectivityTags
data2CleanCut['spicinessTags'] = pd.Series(spicinessTags)

print(data2CleanCut.head(n=100))
# PRISM algorithm module
# Written with <3 and covfefe, Enjoy!

# --- set column name class variable of PRISM here
classVariable = "label"
classResult = "FAKE"
prismFrame = data2CleanCut
# have your featureList be a list of the column names in your dataframe that you want to be part of the PRISM
# do not include the classVariable column in feature list
featureList = list(data2CleanCut)
del featureList[:3]

print(featureList)

#--- Initializing some variables necessary for the PRISM ---
tempFeatureList = featureList
tempPrismFrame = prismFrame
bestConfidence = Fraction(0,1)
featureForBestConfidence = ""
valueForBestConfidence = ""
ruleResult = []

while bestConfidence != 1 or len(tempFeatureList) > 1:

    for feature in tempFeatureList:
        possibleFeatureValues = prismFrame[feature].unique()
        highestConfidence = Fraction(0,1)
        highestTotal = 1
        valueForHighestConfidence = ""

        for value in possibleFeatureValues:
            total = len(tempPrismFrame[tempPrismFrame[feature] == value])
            totalSucceses = len(tempPrismFrame[(tempPrismFrame[feature] == value) & (tempPrismFrame[classVariable] == classResult)])
            print("Number of *" + str(value) + " " + str(feature) + " where " + str(classVariable) + " == " + str(classResult) + " / total number of " + str(value) + "s")
            print (str(totalSucceses) + ' / ' + str(total))

            highestConfidenceCheck = 0
            if total > 0:
                highestConfidenceCheck = Fraction(totalSucceses, total)

            if highestConfidenceCheck > highestConfidence:
                highestConfidence = highestConfidenceCheck
                valueForHighestConfidence = value
            if highestConfidenceCheck == highestConfidence:
                if total > highestTotal:
                    highestConfidence = highestConfidenceCheck
                    valueForHighestConfidence = value
                    highestTotal = total

        print("**** For " + feature + " highest confidence is " + str(highestConfidence) + " for " + feature + " = " + str(valueForHighestConfidence))
        if highestConfidence > bestConfidence:
            bestConfidence = highestConfidence
            featureForBestConfidence = feature
            valueForBestConfidence = valueForHighestConfidence
        # take the one with the highest denominator if two feature values have a confidence of 1
        if highestConfidence == bestConfidence and highestConfidence.denominator < highestTotal:
            bestConfidence = highestConfidence
            featureForBestConfidence = feature
            valueForBestConfidence = valueForHighestConfidence
    ruleResult.append(featureForBestConfidence + " = " + valueForBestConfidence + " -->")
    tempPrismFrame = tempPrismFrame[tempPrismFrame[featureForBestConfidence] == valueForBestConfidence]
    if featureForBestConfidence in tempFeatureList:
        tempFeatureList.remove(featureForBestConfidence)
    else:
        break
ruleResult.append(" then " + classVariable + " is " + classResult)
print(ruleResult)

# write the piece of code where if the highest of high confidences is not 1 grab only the rows where with the highestValue of the highest feauture and repeat on the remaining features

#print(data2CleanCut.head(n=100))
#print(data2CleanCut['polarityTags'])

#remember pytrends Google trends





# classVariable = "label"
# classResult = "FAKE"
# featureList = list(data2CleanCut)
# del featureList[:3]
# print(featureList)
#
# possiblePolarityValues = data2CleanCut.polarityTags.unique()
# print(possiblePolarityValues)
#
# for value in possiblePolarityValues:
#     #print(value)
#     total = len(data2CleanCut[data2CleanCut['polarityTags'] == value])
#     #print(total)
#     totalSucceses = len(data2CleanCut[(data2CleanCut['polarityTags'] == value) & (data2CleanCut[classVariable] == classResult)])
#     print("Number of *" + value + " polarityValues where " + classVariable + " == " + classResult + " / total number of " + value + "s")
#     print (str(totalSucceses) + ' / ' + str(total))




    # for feature in featureList:
    #     possibleFeatureValues = prismFrame[feature].unique()
    #     print(possibleFeatureValues)
    #
    #     highestConfidence = 0
    #     valueForHighestConfidence = ""
    #     for value in possibleFeatureValues:
    #         #print(value)
    #         total = len(prismFrame[prismFrame[feature] == value])
    #         #print(total)
    #         totalSucceses = len(prismFrame[(prismFrame['polarityTags'] == value) & (prismFrame[classVariable] == classResult)])
    #         print("Number of *" + value + " " + feature + " where " + classVariable + " == " + classResult + " / total number of " + value + "s")
    #         print (str(totalSucceses) + ' / ' + str(total))
    #
    #         highestConfidenceCheck = totalSucceses/total
    #         if highestConfidenceCheck > highestConfidence:
    #             highestConfidence = highestConfidenceCheck
    #             valueForHighestConfidence = value
    #
    #     print("**** For " + feature + " highest confidence is " + str(highestConfidence) + " for " + feature + " = " + str(valueForHighestConfidence))
    #     if highestConfidence > bestConfidence:
    #         bestConfidence = highestConfidence
    #         featureForBestConfidence = feature
    #         valueForBestConfidence = valueForHighestConfidence
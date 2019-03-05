import pandas as pd
from datetime import datetime
import sys
import re
from tika import parser #parse pdf text
import numpy as np
from empath import Empath # similar to LIWC
import math
pd.options.mode.chained_assignment = None 



def PostingFreq(file):
    timeFreq = {} #dictionary that shows the average time a user post sth 
    preUser = None #previous user 
    preTime = None #posting time of the previous day
    dayVec = [] #a vector that shows the time difference between a previous day and the day after
    
    for userid, time in zip(file['user_id'], file['timestamp']):
        if preTime is None:
            freq = time 
        elif userid == preUser:
            #freq = previous day - day after
            freq = datetime.strptime(time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(preTime, "%Y-%m-%d %H:%M:%S")
            dayVec.append(freq.days) 
            timeFreq[userid] = dayVec
            
        elif type(freq) is not str and not isinstance(freq, np.float64): # freq is not a datetime object if there is one case only
            dayVec = [freq.days] 

        preTime = time 
        preUser = userid
        
    return timeFreq

def computeMean(dictionary):
    mean = []
    for i in dictionary:
        mean.append((sum(dictionary[i])/len(dictionary[i])))
    return mean

def computeFreq(dictionary):
    freq = []
    for i in dictionary:
        freq.append(len(dictionary[i])+1)
    return freq



def getSlidingWindow(array, window):
    ret = []
    i = 0
    j = window
    while j < len(array):
        ret.append((sum(array[i:j]), i,j))
        i = i+1
        j = j+1
    ret.sort()
    ret.reverse()
    return ret

#if the last time window is 1sd below the mean
def isMoreFrequent(array, window):
    meanlist = []
    for item in getSlidingWindow(array, window):
        meanlist.append(item[0])
    meanL = np.mean(meanlist)
    std = np.std(meanlist)
    result = []
    indexL = []
    for index, item in enumerate(getSlidingWindow(array, window)):
        
        if item[0]  <= meanL - std:
            indexL.append(index)       
    length = len(getSlidingWindow(array, window))-1
    if length != 0:
        if length in indexL:
            return 1
        else:
            return 0
        
def getMoreFrequent(postingFrequency, window):
    results = []
    for item in postingFrequency:
        result = isMoreFrequent(postingFrequency[item],window)
        results.append(result)
    return results

def stringCount(text):
    count = 0
    for item in text.split():
        count = count + 1
    return count 

#this function return a frequency feature matrix 
def getFrequencyFeature(file, intervalName, freqName, isMoreFreq, PostWordCount, SlideWindow): #input df that you need to count the posting frequency and interval 
    #dictionary that shows the average time a user post sth 
    postingFrequency = PostingFreq(file)
    #mean of posting interval
    mean = computeMean(postingFrequency)
    # is the posting behaviour becoming more frequent
    MoreFreq = getMoreFrequent(postingFrequency, SlideWindow)
    #comupte number of postings
    freq = computeFreq(postingFrequency)
    #mean wordcount in post
    PostCount = file.groupby(['user_id']).size().reset_index(name = 'counts')
    file = pd.merge(PostCount, file, on='user_id')
    MoreThanOnePost = file[file.counts > 1]
    MoreThanOnePost['wordCount'] = MoreThanOnePost['post_body'].apply(lambda x: stringCount(str(x)))
    wordCount = MoreThanOnePost.groupby(['user_id'])['wordCount'].mean().reset_index(name = 'counts')
    
    #append all the features
    ProtoDf = np.vstack((list(postingFrequency.keys()),freq))
    ProtoDf = np.vstack((ProtoDf, mean))
    ProtoDf = np.vstack((ProtoDf, MoreFreq))
    ProtoDf = np.vstack((ProtoDf, wordCount.counts))
    df = pd.DataFrame(ProtoDf)
    featureTable = df.T 
    featureTable.columns = ['user_id',freqName,intervalName, isMoreFreq, PostWordCount]
    
    #this part only triggers when there are users posted 1 post
    onePost = PostCount[PostCount.counts == 1]
    one = file[file.counts == 1]
    #now create a table with this one post id, assign NaN to interval and 1 to posting Frequency
    if one.empty is False: 
        one['wordCount'] = one['post_body'].apply(lambda x: stringCount(str(x)))
        onePost[intervalName] = 0
        onePost[isMoreFreq] = 0
        onePost[PostWordCount] = one.wordCount
        onePost.columns = ['user_id', freqName, intervalName, isMoreFreq, PostWordCount]
        featureTable = featureTable.append(onePost,ignore_index=True)
    
    return featureTable


def findText(text, wordList):
    for item in wordList:
        if item in text:
            return True
    return False

def checkDictFea(file):
    file.drop_duplicates(subset=['user_id'], keep=False)
    newFea = file[['user_id']]
    newFea['mentionMethods'] = 1
    return newFea

def readDictionaries(filePath):
    with open(filePath) as f:
        myList = [x.strip().replace("'","").lower() for x in f.read().split(",")]
        #print(Psylist)
    return myList

def subsetDictPosts(file, dictionary, newTitle, newBody, newSubreddit):
    file[newTitle] = file.apply(lambda row: True if findText(row["post_title"], dictionary) else False, axis=1)
    file[newBody] = file.apply(lambda row: True if findText(row["post_body"], dictionary) else False, axis=1)
    file[newSubreddit] = file.apply(lambda row: True if findText(row["subreddit"], dictionary) else False, axis=1)


#path = '/home/lucia/phd_work/shareTask/CLpsych/'
path = '/Users/lucia/phd_work/suicideDetection/'
#file = pd.read_csv(path + '/data_sample_clpsych19/user10146.posts.csv')

file = pd.read_csv('/Users/lucia/phd_work/ClpsyData/clpsych19_training_data/shared_task_posts.csv')
print('step 1')
file['timestamp'] = file['timestamp'].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
FreqTable = getFrequencyFeature(file, 'postingInterval','postingFrequency', 'generalMoreFreq', 'generalWordCount', 6)
FreqTable.to_csv(path+'FreqTable.csv')

# #get text with mental health dictions
print('step 2')
file['post_title'] = file['post_title'].apply(lambda x: x.lower() if type(x) is str else 'NULL')
file['post_body'] = file['post_body'].apply(lambda x: x.lower() if type(x) is str else 'NULL')

# #read dict
PsyList = readDictionaries(path +'/dictionaries/psyList.txt')
print('step 3')
#return boolean table
file['Psy_title'] = file.apply(lambda row: True if findText(row["post_title"], PsyList) else False, axis=1)
file['Psy_body'] = file.apply(lambda row: True if findText(row["post_body"], PsyList) else False, axis=1)


# # #clean text, lower cases
file['post_title'] = file['post_title'].apply(lambda x: x.lower()if type(x) is str else 'NULL')
file['subreddit'] = file['subreddit'].apply(lambda x: x.lower() if type(x) is str else 'NULL')
file['post_body'] = file['post_body'].apply(lambda x: x.lower() if type(x) is str else 'NULL')

#subset data according to boolean
print('step 4')
subsetDictPosts(file, PsyList, 'Psy_title', 'Psy_body', 'Psy_subre')
MH = file[file['Psy_body'] == True]
MHF = getFrequencyFeature(MH, 'healthPostingInterval','healthPostingFrequency', 'healthMoreFreq', 'healthWordCount',3)
#merge features
FreqFea = pd.merge(FreqTable, MHF, on ='user_id', how = 'left')
FreqFea.to_csv(path+'FreqFea.csv1')

print('step 5')
#check suicide methods
SuicideMethods = readDictionaries(path + '/dictionaries/suicideMethods.txt')
subsetDictPosts(file, SuicideMethods, 'med_title', 'med_body', 'med_subre')
#we only check if suicidewatch posts contain these keywords
suicideWatch = file[file['subreddit'] == 'suicidewatch']
med = suicideWatch[(suicideWatch['med_body'] == True) | (suicideWatch['med_title'] == True)]

#get suicideWatch post
SW = file[file['subreddit'] == 'suicidewatch']
SWFreq = getFrequencyFeature(SW, 'SWPostingInterval','SWFrequency', 'SWFreq', 'SWWordCount',3)


#return feature table
methods = checkDictFea(med) 
#merge features
FreqFea = pd.merge(FreqFea, methods, on ='user_id', how = 'left')
FreqFea = pd.merge(FreqFea, SWFreq, on ='user_id', how = 'left')
FreqFea.fillna(0, inplace=True)

FreqFea.to_csv(path+'FreqFea.csv')














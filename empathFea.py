import pandas as pd
from datetime import datetime
import sys
import re
from tika import parser #parse pdf text
import numpy as np
from empath import Empath # similar to LIWC
import math
pd.options.mode.chained_assignment = None 
import glob

def readDictionaries(filePath):
    with open(filePath) as f:
        myList = [x.strip().replace("'","").lower() for x in f.read().split(",")]
        #print(Psylist)
    return myList


def findText(text, wordList):
    for item in wordList:
        if item in text:
            return True
    return False

def subsetDictPosts(file, dictionary, newTitle, newBody, newSubreddit):
    file[newTitle] = file.apply(lambda row: True if findText(row["post_title"], dictionary) else False, axis=1)
    file[newBody] = file.apply(lambda row: True if findText(row["post_body"], dictionary) else False, axis=1)
    file[newSubreddit] = file.apply(lambda row: True if findText(row["subreddit"], dictionary) else False, axis=1)


def getEmpath(file):
    empathy = {}
    for item, postid in zip(file['post_body'],file['post_id']):
        empathy[postid] = lexicon.analyze(item, normalize=True) 
    empathyFea = pd.DataFrame.from_dict(empathy)
    empathyFea = empathyFea.T
    empathyFea['post_id'] = empathyFea.index
    return empathyFea

def getDictionsEmpath(file, PsyList, EmpathVars):
    subsetDictPosts(file, PsyList, 'Psy_title', 'Psy_body', 'Psy_subre')
    subset = file[(file['Psy_body'] == True) | (file['Psy_title'] == True) | (file['Psy_subre'] == True)]
    Features = getEmpath(subset)
    Fea = pd.merge(subset, Features, on = 'post_id', how ='left')
    empathFea = Fea[EmpathVars]
    #aggregate to user level 
    empath = empathFea.groupby('user_id').mean()
    return empath

#this function gets the general empath score 
def getGeneralEmpath(file, EmpathVars):
    Features = getEmpath(file)
    Fea = pd.merge(file, Features, on = 'post_id', how ='left')
    empathFea = Fea[EmpathVars]
    #aggregate to user level 
    empath = empathFea.groupby('user_id').mean()
    return empath

def lowerCase(file):
    file['post_title'] = file['post_title'].apply(lambda x: x.lower() if type(x) is str else 'NULL')
    file['subreddit'] = file['subreddit'].apply(lambda x: x.lower() if type(x) is str else 'NULL')
    file['post_body'] = file['post_body'].apply(lambda x: x.lower() if type(x) is str else 'NULL')
    return file

def mergeFrames(pathTofile):
    allFiles = glob.glob(pathTofile)

    list_ = []

    for file_ in allFiles:
        df = pd.read_csv(file_,index_col=None, header=0)
        list_.append(df)
    
    frame = pd.merge(list_[0], list_[1], on = 'user_id', how = 'outer')
    if len(list_)-1 > 2:
        n = len(list_)-1
        while n > 1:
            frame = pd.merge(frame, list_[n], on = 'user_id', how = 'outer')
            # frame = frame2
            n = n-1
    # else:
    #     frame2 = frame
    # # n = 3
    # while n < len(list_):
    #     ...
    #.    n = n+1 
            
    frame.fillna(0, inplace=True)
    frame.to_csv(path+"/features/emPathFea/Merged.csv")
    return frame


lexicon = Empath()

print('step 1')
path = '/Users/lucia/phd_work/suicideDetection/'
#file = pd.read_csv(path + '/SampleShareTask/test.csv')
file = pd.read_csv('/Users/lucia/phd_work/ClpsyData/clpsych19_training_data/shared_task_posts.csv')


PsyList = readDictionaries(path +'/dictionaries/psyList.txt')
file = lowerCase(file)

#define dictionary and the empath topics you want to retain
EmpathVars = ['post_id','user_id', 'achievement', 'shame', 'affection', 'aggression', 'anger', 'cheerfulness', 'disappointment', 'disgust', 'dispute', 'emotional', 'fear', 'fun', 'hate', 'joy', 'love', 'negative_emotion', 'nervousness', 'optimism', 'pain', 'positive_emotion', 
                 'suffering', 'alcohol', 'appearance', 'attractive', 'banking', 'money', 'body', 'health', 'injury', 'medical_emergency', 'death', 'friends', 'help']

EmpathVars1 = ['post_id','user_id', 'anger', 'disappointment', 'negative_emotion', 'health', 'injury', 'medical_emergency', 'death']

print('step 2')
fea = getDictionsEmpath(file, PsyList, EmpathVars1)
print('step 3')
feaAll = getGeneralEmpath(file, EmpathVars)

fea.to_csv(path+'/features/emPathFea/fea.csv')
feaAll.to_csv(path+'/features/emPathFea/feaAll.csv')



#mergeFrames(path + "/features/emPathFea/*.csv")


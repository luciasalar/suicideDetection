# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 07:41:23 2019

@author: Abeer
"""

import pandas as pd
from datetime import datetime
import sys
import re
import numpy as np
from empath import Empath 






#training features set for each user 
def similarity_between_the_freq_vec(vec):
    print("calc")


#frequency of posting 
def PostingFreq(file):
    #timeFreq = {} #dictionary that shows the average time a user post sth 
    timeFreq= []
    #preUser = None #previous user 
    preTime = None #posting time of the previous day
    dayVec = [] #a vector that shows the time difference between a previous day and the day after
    
    for userid, time in zip(file['user_id'], file['timestamp']):
        if preTime is None:
            freq = time 
        else:
        #elif userid == preUser:
            #freq = previous day - day after
            freq = datetime.strptime(time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(preTime, "%Y-%m-%d %H:%M:%S")
            dayVec.append(freq.days) 
            #timeFreq[userid] = dayVec
            timeFreq = dayVec
            
        if type(freq) is not str: # freq is not a datetime object if there is one case only
            dayVec = [freq.days] 

        preTime = time 
        #preUser = userid
        
    return timeFreq

#here we compute the mean of posting interval 
def computeMean(dictionary):
    mean = []
    for i in dictionary:
        mean.append((sum(dictionary[i])/len(dictionary[i])))
    return mean


#we can also get the frequency 
def computeFreq(dictionary):
    freq = []
    for i in dictionary:
        freq.append(len(dictionary[i])+1)
    return freq



def getSentiVec(usercollection):
    print("in process of building senti eval")
    #In process of comparing diferent sentiment results 
    


#This function initiate the training and testing files
def Features_constructor( training_file,testing_file):      
    training_data = pd.read_csv(training_file, sep=',', encoding='latin1', low_memory=False) 
    users_ids=training_data["UserID"]
    #print(users_ids[3])
    print("training shape")
    print(training_data.shape)
    
    features_values_peruser={}
    #Features_dictionary={"123":{'mean_time':3}}
    Features_dictionary={}
    
    
    
    for i in range (0,len(users_ids)):
        #get the user's file (posts collection)
        userfile=pd.read_csv("C:/Users/Abeer/Dropbox/clpsych_workshop/data_sample_clpsych19/user"+str(users_ids[i])+".posts.csv", sep=',', encoding='latin1', low_memory=False)        
        userfile['timestamp'] = userfile['timestamp'].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
    
        #Freuency of user's posting
        freqvec=PostingFreq(userfile)
        print(freqvec)
        freqmean= sum(freqvec)/len(freqvec)
        print(freqmean) 
        
        #save value in the features dictionar 
        features_values_peruser["postingFrequency"]=freqmean
        
        #------------------------------------------
        #sentiment vector
        
        sentimentvec=getSentiVec(userfile)
        
        Features_dictionary[str(users_ids[i])]=features_values_peruser
        features_values_peruser={}
        
    
    #print(Features_dictionary["123"]["mean_time"])
    
    #this file generate the training/testing features in new file
    prepare_file_features(Features_dictionary,training_data)
   


def prepare_file_features(Features,file):
    
    new_CSV_file="C:/Users/Abeer/Dropbox/clpsych_workshop/Training_features.csv"
    file_new= open(new_CSV_file,'w')
    new_test_df = pd.read_csv(new_CSV_file, sep=',',encoding='latin1',names=["UserID","mean_time", "Risk_Level"])
    
    #convert timestamp to time

    index=0
    for y in Features:
        
        userID= file.at[index,'UserID']
        risk_level= file.at[index,'Risk_Level']        
        new_test_df.loc[index, 'UserID'] = userID
        new_test_df.loc[index, 'Risk_Level'] =risk_level
        
        #features
        new_test_df.loc[index, 'postingFrequency']=Features[str(userID)]["postingFrequency"]
        
                   
        index=index+1
        
    new_test_df.to_csv("C:/Users/Abeer/Dropbox/clpsych_workshop/Training_features.csv", index=False,sep=',') 
    file_new.close()




if __name__ == '__main__':
    
   training_file="C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/training_clpsych.csv"
   Testing_file="C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/testing_clpsych.csv"
 
   Features_constructor(training_file,Testing_file)
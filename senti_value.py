# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 16:16:21 2019

@author: Abeer
"""

import subprocess
import shlex
import pandas as pd 
def RateSentiment(sentiString):
    #open a subprocess using shlex to get the command line string into the correct args list format
    #Modify the location of SentiStrength.jar and D:/SentiStrength_Data/ if necessary
    p = subprocess.Popen(shlex.split("java -jar C:/Users/Abeer/Dropbox/clpsych_workshop/SentiStrength.jar stdin sentidata C:/Users/Abeer/Dropbox/clpsych_workshop/SentiStrength_Data/"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #communicate via stdin the string to be rated. Note that all spaces are replaced with +
    
    print(sentiString)
    sentiString=str(sentiString)
    #Can't send string in Python 3, must send bytes
    b = bytes(sentiString.replace(" ","+"), 'utf-8')
    stdout_byte, stderr_text = p.communicate(b)
    #convert from byte
    stdout_text = stdout_byte.decode("utf-8") 
    
    #replace the tab with a space between the positive and negative ratings. e.g. 1    -5 -> 1 -5
    stdout_text = stdout_text.rstrip().replace("\t"," ")
    print(stdout_text)
    
    return stdout_text
#An example to illustrate calling the process.


def prepare_file_features(senti_list,userid):
    original_posts_file="C:/Users/Abeer/Dropbox/clpsych_workshop/data_sample_clpsych19/user"+str(users_ids[i])+".posts.csv"
    original_posts_df = pd.read_csv(original_posts_file, sep=',',encoding='latin1')
    
    
    new_CSV_file="C:/Users/Abeer/Dropbox/clpsych_workshop/data_sample_clpsych19/user"+str(users_ids[i])+"_posts_sentiment.csv"
    file_new= open(new_CSV_file,'w')
    new_test_df = pd.read_csv(new_CSV_file, sep=',',encoding='latin1',names=["post_id",	"user_id",	"timestamp",	"subreddit"	,"post_title",	"post_body" , "sentiment"])
    
    #convert timestamp to time

    index=0
    for sentiments in senti_list:
        print(sentiments)
        sentiment_results=sentiments.split(" ")
        positive_strength=int(sentiment_results[0])
        negative_strength=int(sentiment_results[1])
        print("negative_strength")
        print (negative_strength)
        negative_strength=negative_strength * -1
        print(negative_strength)
        
        finalSentimint=""
        
        if positive_strength>negative_strength:
            finalSentimint='pos'
            print("positive result "+ str(positive_strength) + "other "+str(negative_strength))
        elif positive_strength<negative_strength: 
            finalSentimint='neg'
            print("negative result "+ str(negative_strength))
        else:
            finalSentimint='nut' #nutral
        
        #post_id	user_id	timestamp	subreddit	post_title	post_body
        post_id=original_posts_df.at[index,'post_id']
        userID= original_posts_df.at[index,'user_id']
        timestamp= original_posts_df.at[index,'timestamp'] 
        subreddit= original_posts_df.at[index,'subreddit'] 
        post_title= original_posts_df.at[index,'post_title'] 
        post_body= original_posts_df.at[index,'post_body']
             
        
        
        new_test_df.loc[index, 'post_id'] = post_id
        new_test_df.loc[index, 'user_id'] =userID
        new_test_df.loc[index, 'timestamp'] = timestamp
        new_test_df.loc[index, 'subreddit'] =subreddit
        new_test_df.loc[index, 'post_title'] = post_title
        new_test_df.loc[index, 'post_body'] =post_body
        new_test_df.loc[index, 'sentiment'] = finalSentimint
                   
        index=index+1
        
    new_test_df.to_csv(new_CSV_file, index=False,sep=',') 
    file_new.close()



if __name__ == '__main__':
    
    training_file="C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/training_clpsych.csv"
    Testing_file="C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/testing_clpsych.csv"
    
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
        postslist=userfile['post_body']
        
        list_senti_strength_user=[]
        for post in postslist:
            if post is None:
                list_senti_strength_user.append("")
            else:    
                list_senti_strength_user.append(RateSentiment(post))
                
                
        #after analyzing the sentiment for each user we will save the new results in new user file    
        prepare_file_features(list_senti_strength_user,str(users_ids[i]))


#The above is OK for one text but inefficient to repeatedly call for many texts. Try instead: 
#  either modify the above to submit a file
#  or modify the above to send multiple lines through multiple calls of p.communicate(b)


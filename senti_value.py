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


def prepare_file_features(senti_list,userfile):
    #="C:/Users/Abeer/Dropbox/clpsych_workshop/data_sample_clpsych19/user"+str(users_ids[i])+".posts.csv"
    original_posts_df = pd.read_csv(userfile, sep=',',encoding='latin1')    
    
    new_CSV_file="C:/Users/Abeer/Dropbox/clpsych_workshop/data_sample_clpsych19/posts_sentiment.csv"
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
        
        Crowd_users="C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/clpsych19_training_data/clpsych19_training_data/crowd_train.csv"
        
        #Testing_file="C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/testing_clpsych.csv"
    
        training_crowd_data = pd.read_csv(Crowd_users, sep=',', encoding='latin1', low_memory=False) 
        users_ids=training_crowd_data["UserID"]
        
        #list of post of task B as provided by the organizers (no SW posts)
        post_taskB= "C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/clpsych19_training_data/clpsych19_training_data/task_B_train.posts.csv"
        Task_B_posts=pd.read_csv(post_taskB, sep=',', encoding='latin1', low_memory=False) 
        
        users_ids=Task_B_posts["user_id"]
        
        for users in users_ids:
            Pos_ids_user=Task_B_posts.loc[(Task_B_posts["user_id"] == Task_B_posts) & (training_data['Stance'] == 'supporting') ]

        #list of the posts texts for the users
        
        userfile=pd.read_csv("C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/clpsych19_training_data/clpsych19_training_data/shared_task_posts.csv", sep=',', encoding='latin1', low_memory=False)        
        postslist=userfile['post_body']
        ##the sentiment of 10,48576 records 
        
        #loop over each user id in the main crowd user 
        for user_id in users_ids:            
            
            #the sentiment of 10,48576 records 
            list_senti=[]
            for post in postslist:
                if post is None:
                    list_senti.append("")
                else:    
                    list_senti.append(RateSentiment(post))
                    
                    
            #after analyzing the sentiment for each user we will save the new results in new user file
            prepare_file_features(list_senti,userfile)
       

#The above is OK for one text but inefficient to repeatedly call for many texts. Try instead: 
#  either modify the above to submit a file
#  or modify the above to send multiple lines through multiple calls of p.communicate(b)


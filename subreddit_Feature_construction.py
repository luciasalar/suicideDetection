# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:10:26 2019

@author: Abeer
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 09:24:05 2019

@author: Abeer
"""
import pandas as pd 
import os


def prepare_features_file(dic_values) :
    new_CSV_file="C:/Users/Abeer/Dropbox/clpsych_workshop/Training_features_sentiment_subreddits.csv"
    
    file_new= open(new_CSV_file,'w')
    new_test_df = pd.read_csv(new_CSV_file, sep=',',encoding='latin1',names=["user_id","sentiment_score","subreddits","raw_label"])    
    
    
    
    file_data=pd.read_csv("C:/Users/Abeer/Dropbox/clpsych_workshop/Training_features_sentiment.csv", sep=',', encoding='latin1', low_memory=False)        
    usersIds=  file_data["user_id"]
    #convert timestamp to time

    index=0
    for y in usersIds:
        
        userID= file_data.at[index,'user_id']
        risk_level= file_data.at[index,'raw_label']   
        senti_score= file_data.at[index,'sentiment_score']   
        new_test_df.loc[index, 'user_id'] = userID
        new_test_df.loc[index, 'raw_label'] =risk_level 
        new_test_df.loc[index, 'sentiment_score'] =senti_score  
        subreddits=dic_values[userID] 
        subreddits=" ".join(str(val) for val in subreddits)
        print(subreddits)
        new_test_df.loc[index,'subreddits']=subreddits
                   
        index=index+1
        
    new_test_df.to_csv("C:/Users/Abeer/Dropbox/clpsych_workshop/Training_features_sentiment_subreddits.csv", index=False,sep=',') 
    file_new.close()





if __name__=='__main__':
    
    #loop over sentiment 
    Crowd_users="C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/clpsych19_training_data/clpsych19_training_data/crowd_train.csv"      
    #Testing_file="C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/testing_clpsych.csv"    
    training_crowd_data = pd.read_csv(Crowd_users, sep=',', encoding='latin1', low_memory=False) 
    users_ids=training_crowd_data["user_id"]    
    #list of post of task B as provided by the organizers (no SW posts)
    post_taskB= "C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/clpsych19_training_data/clpsych19_training_data/task_B_train.posts.csv"
    Task_B_posts=pd.read_csv(post_taskB, sep=',', encoding='latin1', low_memory=False) 
    users_ids=Task_B_posts["user_id"]
    userfile=pd.read_csv("C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/clpsych19_training_data/clpsych19_training_data/shared_task_posts.csv", sep=',', encoding='latin1', low_memory=False)            
    postslist=userfile    
    Matrix_values=[]
    users_values=[]
    
    dic_values={}
    
    
    users_ids=list(set(users_ids))
    for main_user in users_ids:
        list_subreddit=[]
        #main_user=int(main_user)
        posts=Task_B_posts[Task_B_posts["user_id"] == main_user]
        print(Task_B_posts)
        posts_category=[val for val in posts["subreddit"]]
        print(posts_category)
        dic_values[main_user]=posts_category
        
        
    prepare_features_file(dic_values)   
        #convert timestamp to time
# start calculating the score between two users sentiment values 
    

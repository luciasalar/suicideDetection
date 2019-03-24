# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 09:24:05 2019

@author: Abeer
"""
import pandas as pd 
import os


def prepare_file_sentiments(users_ids,dic_values) :
    new_CSV_file="C:/Users/Abeer/Dropbox/clpsych_workshop/Sentiment_files/posts_sentiment_values_test.csv"
    
    file_new= open(new_CSV_file,'w')
    new_test_df = pd.read_csv(new_CSV_file, sep=',',encoding='latin1',names=["user_id","sentiment"])    
    
    index=0
    
    keys_lis=dic_values.keys()
     
    for val in keys_lis:
        new_test_df.loc[index, 'user_id'] = val
        new_test_df.loc[index, 'sentiment'] = dic_values[val]
        index=index+1
        
    new_test_df.to_csv(new_CSV_file, index=False,sep=',') 
    file_new.close()

        
        
        

def levenshtein_distance(a, b):
    """Return the Levenshtein edit distance between two strings *a* and *b*."""
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    if not a:
        return len(b)
    previous_row = range(len(b) + 1)
    for i, column1 in enumerate(a):
        current_row = [i + 1]
        for j, column2 in enumerate(b):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (column1 != column2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1] 



if __name__=='__main__':
    
    #loop over sentiment 
    Crowd_users="C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/clpsych19_training_data/clpsych19_training_data/crowd_train.csv"      
    #Testing_file="C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/testing_clpsych.csv"    
    training_crowd_data = pd.read_csv(Crowd_users, sep=',', encoding='latin1', low_memory=False) 
    users_ids=training_crowd_data["user_id"]    
    #list of post of task B as provided by the organizers (no SW posts)
    post_taskB= "C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/clpsych19_training_data/clpsych19_testing_data/task_B_test.posts.csv"
    Task_B_posts=pd.read_csv(post_taskB, sep=',', encoding='latin1', low_memory=False) 
    users_ids=Task_B_posts["user_id"]
    userfile=pd.read_csv("C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/clpsych19_training_data/clpsych19_testing_data/shared_task_posts_test.csv", sep=',', encoding='latin1', low_memory=False)            
    postslist=userfile    
    Matrix_values=[]
    users_values=[]
    
    dic_values={}
    
    #----------------------user id------------------
    coulm_id=[]
    users_ids_file='C:/Users/Abeer/Dropbox/clpsych_workshop/Sentiment_files_test/'
    for filename in os.listdir(users_ids_file):
     if filename.endswith('.csv'):
        userID= filename.replace('posts_sentiment_test','')
        userID=userID.replace('.csv','')
        userID=userID.replace('\n',"")
        coulm_id.append(userID)
        

    average_value=0
    edit_score=[]
    # get the result for every user in the dataset 
    users_ids=list(set(users_ids))
    for main_user in users_ids:
        sentistring_main=""
        new_CSV_file="C:/Users/Abeer/Dropbox/clpsych_workshop/Sentiment_files_test/posts_sentiment_test"+str(main_user)+".csv"
        file_new= open(new_CSV_file,'r')
        new_test_df = pd.read_csv(new_CSV_file, sep=',',encoding='latin1',names=["post_id","sentiment"])            
        sentimentvalues=new_test_df['sentiment']
        sentistring_main= ''.join(str(val) for val in sentimentvalues)                        
        print(main_user)
        edit_score=[]
        for user_column in coulm_id:
            sentistring_2=""
            new_CSV_file="C:/Users/Abeer/Dropbox/clpsych_workshop/Sentiment_files_test/posts_sentiment_test"+str(user_column)+".csv"
            file_new= open(new_CSV_file,'r')
            new_test_df = pd.read_csv(new_CSV_file, sep=',',encoding='latin1',names=["post_id","sentiment"])    
            
            sentimentvalues=new_test_df['sentiment']
            sentistring_2= ''.join(str(val) for val in sentimentvalues)
            edit_score.append(levenshtein_distance(sentistring_main, sentistring_2))
            
            
        
        
        sum_values= sum(edit_score)  
        average_value= sum_values/len(edit_score)
        print(average_value)
        dic_values[main_user]=average_value
    
    
    
    prepare_file_sentiments(users_ids,dic_values)     
        #convert timestamp to time
# start calculating the score between two users sentiment values 
    

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 15:37:47 2019

@author: Abeer
"""

import praw
import pandas as pd
import praw.exceptions  as exp
#from urllib import HTTPError
import requests
#url  https://stackoverflow.com/questions/36366388/get-all-comments-from-a-specific-reddit-thread-in-python
reddit = praw.Reddit(client_id='JQNYlic9hrdOmQ',
                     client_secret='EnK47Bx63Zh6S_nOKyDZIIPy9Ls',
                     password='1548Ou38237',
                     user_agent='N_processing',
                     username='AbeerID ')

#print(reddit.user.me())


def get_the_commenters(training_file):
    
    
    training_data = pd.read_csv(training_file, sep=',', encoding='latin1', low_memory=False) 
    users_ids=training_data["UserID"]
    #print(users_ids[3])
    print("training shape")
    print(training_data.shape)
    
    
    
    for i in range (0,len(users_ids)):
        #get the user's file (posts collection)
        userfile=pd.read_csv("C:/Users/Abeer/Dropbox/clpsych_workshop/data_sample_clpsych19/user"+str(users_ids[i])+".posts.csv", sep=',', encoding='latin1', low_memory=False)        
        postIDList=userfile["post_id"]
        #this dictionary contains the post comments pair 
        posts_comments={}
        #author of the comments to populate the list
        author_list=[]
        try:
            for postID in postIDList:           
                #res = getAll(r, "e5db6")
                print(reddit.submission(id=postID).title)
                submission = reddit.submission(id=postID)
                for top_level_comment in submission.comments:
                    author_list.append(str(top_level_comment.author))
                    #author
                    print(top_level_comment.author)
                posts_comments[postID]=author_list
                author_list=[]   
            prepare_file_commenter_features(posts_comments,users_ids[i])
        except requests.HTTPError as e:  # pragma: no cover
            print("error handler")
            author_list.append("none")
            continue
                   
            
         
        #user level
         

def prepare_file_commenter_features(listofcomments,userid):
    original_posts_file="C:/Users/Abeer/Dropbox/clpsych_workshop/data_sample_clpsych19/user"+str(userid)+".posts.csv"
    original_posts_df = pd.read_csv(original_posts_file, sep=',',encoding='latin1')
    
    
    new_CSV_file="C:/Users/Abeer/Dropbox/clpsych_workshop/data_sample_clpsych19/user"+str(userid)+"_posts_commenters.csv"
    file_new= open(new_CSV_file,'w')
    new_test_df = pd.read_csv(new_CSV_file, sep=',',encoding='latin1',names=["post_id",	"user_id",	"timestamp",	"subreddit"	,"post_title",	"post_body" , "commenters"])
    
   

    index=0
    listofKeys=list(listofcomments.keys())
    for commentsinpost in range(len(listofcomments)):
        postID=listofKeys[index]
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
        new_test_df.loc[index, 'commenters'] = listofcomments[postID]
                   
        index=index+1
        
    new_test_df.to_csv(new_CSV_file, index=False,sep=',') 
    file_new.close()
        

    
if __name__ == '__main__':   
   training_file="C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/training_clpsych.csv"
   Testing_file="C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/testing_clpsych.csv"
 
   get_the_commenters(training_file)
   
   
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 07:41:23 2019

@author: Abeer
"""


from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
#from sklearn import cross_validation
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold 
#from sklearn.model_selection import KFold
from sklearn.feature_extraction import text

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn import svm
from sklearn.svm import LinearSVC # for multi-classification (3 classes)
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion

from sklearn.metrics import classification_report
# call the file training and testing

import pandas as pd
#import pdb
#from IPython.core.debugger import Tracer


#classify the risck of a sucide 


#------------------------------------------------
class SentimentExtractor(BaseEstimator, TransformerMixin):
    """Takes in dataframe, extracts road name column, outputs average word length"""

    

    
    def __init__(self):
        pass

    def Sent_map(self, name):
        """Helper code to compute average word length of a name"""
        print(name)
        if name=='POSITIVE':
         print ('pos')
         return 2
        elif name=='NEGATIVE':
         print ('neg')
         return 1
        else:
         return 0
        

    def transform(self, df, y=None):
        """The workhorse of this feature extractor"""
        s=df['Sent'].apply(self.Sent_map)
        return s.values.reshape(-1,1)

    def fit(self, df, y=None):
        """Returns `self` unless something different happens in train and test"""
        return self

class SentimentScoreExtractor_Positive(BaseEstimator, TransformerMixin):
    """Takes in dataframe, extracts road name column, outputs average word length"""

    def __init__(self):
        pass

          
    def transform(self, df, y=None):
        """The workhorse of this feature extractor"""
        s=df['Positive']
        return s.values.reshape(-1,1)

    def fit(self, df, y=None):
        """Returns `self` unless something different happens in train and test"""
        return self

class SentimentScoreExtractor_NEG(BaseEstimator, TransformerMixin):
    """Takes in dataframe, extracts road name column, outputs average word length"""

    def __init__(self):
        pass

    def Sent_map(self, name):
        """Helper code to compute average word length of a name"""
        #print(name)
        
        return (name*-1)
        

    def transform(self, df, y=None):
        """The workhorse of this feature extractor"""
        s=df['Negative'].apply(self.Sent_map)
        return s.values.reshape(-1,1)

    def fit(self, df, y=None):
        """Returns `self` unless something different happens in train and test"""
        return self

class ItemSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data_dict):
        #print(data_dict[self.key])
        for t in data_dict[self.key]:
            #print(t)
            return data_dict[self.key]

#-------------------------------------------------
#Intiate the model and build the features vectors
def start(target, training_file,testing_file):      
    training_data = pd.read_csv(training_file, sep=',', encoding='latin1', low_memory=False)
    
   
    print("training shape")
    print(training_data.shape)
    
    #'latin1'
    #utf-8
    print("----------------------------------")
    dev_data = pd.read_csv(testing_file,  sep=',', encoding='latin1',low_memory=False)
    print("Testing shape")
    print(dev_data.shape)
    
   
    
    
    #-----------training feature-----------------------
    my_stopword_list= text.ENGLISH_STOP_WORDS
    Y_train = np.asarray([riskLevel for riskLevel in training_data['riskLevel']]) 
    Y_eval = np.asarray([riskLevel for riskLevel in dev_data['riskLevel']])
    my_stopword_list
    # build the feature matrices
    
    main_post= Pipeline([
                    ('selector', ItemSelector(key='main_post')),
                    ('tfidf', CountVectorizer(analyzer='word',binary=True,ngram_range=(1,1))),
                ])
    
   
    
    ppl = Pipeline([
      
        
         ('feats', FeatureUnion([
                 ('main_post',main_post)
      #('Sentiment', SentimentExtractor())
   
    

    #,
     # ('sentiment_score_positive',SentimentScoreExtractor_Positive())
     #,
     #('sentiment_score_Negative',SentimentScoreExtractor_NEG())
      ]))
       #, # or a transformer
          # can pass in either a pipeline
         
      #  ('clf', SVC(kernel='linear',class_weight='balanced', C=1.0, random_state=0))  # baseline classifier
       ,('clf', SVC(kernel='linear',class_weight='balanced') ) # baseline classifier with cross fold 5 
    ])    
    
        
    #different parameter to explore with:
    #parameters = {'clf__C':[5]} 
    #{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],'C': [1, 10, 100, 1000]},
    #tuned_parameters = [{'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
    tuned_parameters = { 'clf__C': [1, 10, 5,100, 1000,10000]}

#    model=sklearn.grid_search.GridSearchCV(ppl, param_grid=tuned_parameters,cv=5)
#    print(model.get_feature_names())
#    print(model.best_params_)
    model = ppl.fit(training_data, Y_train)
    model.fit(training_data, Y_train)

    print(model.classes_)
#new print
    #print(ppl.classes_)
    # test the classifier
    #cross_validation.cross_val_score(clf, X_vec, y, cv=2)
    #scores = cross_validation.cross_val_score(ppl, iris.data, iris.target, cv=5)

    y_test = model.predict(dev_data)
    print(classification_report(Y_eval, y_test))    
    
    
    prepare_file_output(y_test,target,dev_data)
    
    
   


def prepare_file_output(y_values,target,test_df,index):
    print("prepare resulting file output")
   
    
    new_CSV_file="C:/Users/Abeer/Dropbox/PHD/models/resultfile.csv"
    file_new= open(new_CSV_file,'w')
    new_test_df = pd.read_csv(new_CSV_file, sep=',',encoding='latin1',names=["UserID", "RiskLevel"])
    
   
    for y in y_values:
        
        User_ID= test_df.at[index,'UserID']
        
        
        new_test_df.loc[index, 'UserID'] = str(User_ID)
        new_test_df.loc[index, 'RiskLevel'] = str(y)
                   
        index=index+1
        
    new_test_df.to_csv("C:/Users/Abeer/Dropbox/PHD/models/resultfile.csv", index=False,sep=',') 
    file_new.close()




if __name__ == '__main__':
    
   training_file="C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/training_clpsych.csv"
   Testing_file="C:/Users/Abeer/Dropbox/clpsych_workshop/Training_Testing/training_clpsych.csv"
   
   start(training_file,Testing_file)
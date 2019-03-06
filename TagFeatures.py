import pandas as pd
import nltk
from nltk.tokenize import word_tokenize



#this script retrieve the avrage number of tags from each user
def getTagDict(file):
    tagDict ={}
    for text, postID, userID  in zip(file['post_body'], file['post_id'],file['user_id']):
        Tagtext = word_tokenize(str(text))
        tagDict[postID] = nltk.pos_tag(Tagtext)
    return tagDict

def getTagCounts(file):
    
    tagCountDict ={}
    tagDict = getTagDict(file)
    for key, val in tagDict.items():
        tagList =[]
        for item in val:
            tagList.append(item[1])
        #print(len(tagList)) normalize by number of words 
        tagCountDict[key] = [tagList.count('NN')/len(tagList), tagList.count('NNS')/len(tagList), tagList.count('JJR')/len(tagList), tagList.count('MD')/len(tagList),tagList.count('NNP')/len(tagList),
                            tagList.count('NNPS')/len(tagList),tagList.count('PDT')/len(tagList),tagList.count('POS')/len(tagList),tagList.count('PRP')/len(tagList),tagList.count('PRP$')/len(tagList),
                            tagList.count('VB')/len(tagList),tagList.count('VBD')/len(tagList),tagList.count('VBG')/len(tagList),tagList.count('VBN')/len(tagList), tagList.count('VBZ')/len(tagList)]   

    return tagCountDict

def getUserTagCounts(file):
    tagCount = getTagCounts(file)
    tagCountDf = pd.DataFrame.from_dict(tagCount)
    tagCountDf =  tagCountDf.T
    tagCountDf.columns = ['NN','NNS','JJR','MD','NNP','NNPS','PDT','POS','PRP','PRP$','VB','VBD','VBG','VBN','VBZ']
    tagCountDf['post_id'] = tagCountDf.index
    userid = file[['user_id','post_id']]
    userTag = pd.merge(tagCountDf, userid, on = 'post_id')
    userTagCount = userTag.groupby('user_id').mean().reset_index()
    return userTagCount


path =  '/Users/lucia/phd_work/Clpsy/'
file = pd.read_csv(path + 'suicideDetection/sample.csv')
userTags = getUserTagCounts(file)
userTags.to_csv(path + 'suicideDetection/features/TagFea.csv')








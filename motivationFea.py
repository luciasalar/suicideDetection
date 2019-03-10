import pandas as pd 
import re

def preprocess(sent):

    words = str(sent).split()
    new_words = []

    for w in words:
        # remove non English word characters
        w = re.sub(r'[^\x00-\x7F]+',' ', w).lower()
        # remove puncutation 
        w = re.sub(r'[^\w\s]','',w)
        #remove digits
        w = re.sub(r'[0-9]+', '', w)  
   
        new_words.append(w)
        
    return ' '.join(new_words)

def readDictionaries(filePath):
    with open(filePath) as f:
        myList = [x.strip().replace("'","").lower() for x in f.read().split(",")]
        #print(Psylist)
    return myList


def lowerCase(file):
    file['post_body'] = file['post_body'].apply(lambda x: x.lower() if type(x) is str else 'NULL')
    return file


#if words find in text, print 'T', otherwise 'F'
def findText(text, wordList):
    for item in wordList:
        if item in text:
            return True
    return False

def subsetDictPosts(file, dictionary, newBody):
    file[newBody] = file.apply(lambda row: 1 if findText(row["post_body"], dictionary) else 0, axis=1)
    newFile = file[['user_id',newBody]]
    return newFile 


path = path =  '/Users/lucia/phd_work/Clpsy/'
file = pd.read_csv(path + 'data/clpsych19_training_data/Btrain_NoNoise_SW.csv')

print('join all the posts on user level')
file['post_body'] = file['post_body'].apply(lambda x: preprocess(x))
file = file.groupby('user_id').post_body.apply(lambda x: x.sum()).reset_index()

print('read dictionaries')
lowerFile = lowerCase(file)
FinancialList = readDictionaries(path +'suicideDetection/dictionaries/financial_problems.txt')
illegalDrugList = readDictionaries(path +'suicideDetection/dictionaries/illegalDrugs.txt')
mentalHealthList = readDictionaries(path +'suicideDetection/dictionaries/mentalHealth.txt')
relationshipProblems = readDictionaries(path +'suicideDetection/dictionaries/relationshipProblems.txt')
suicideMethods = readDictionaries(path +'suicideDetection/dictionaries/suicideMethods.txt')


print('check wordList')
FinancialProblems = subsetDictPosts(file, FinancialList,  'fin_body')
illegalDrugProblems = subsetDictPosts(file, illegalDrugList, 'drug_body')
mentalHealthProblems = subsetDictPosts(file, mentalHealthList,  'mental_body')
relationshipProblems = subsetDictPosts(file, relationshipProblems,  'rela_body')
suicideMethods = subsetDictPosts(file, suicideMethods, 'suicide_body')

print('merge results')
motivations = pd.merge(FinancialProblems, illegalDrugProblems, on = 'user_id')
motivations = pd.merge(motivations, mentalHealthProblems, on = 'user_id')
motivations = pd.merge(motivations, relationshipProblems, on = 'user_id')
motivations = pd.merge(motivations, suicideMethods, on = 'user_id')
motivations['motivations'] = motivations.iloc[:,1:5].sum(axis = 1, skipna = True) 

motivations.to_csv(path + 'suicideDetection/features/motivations.csv' )













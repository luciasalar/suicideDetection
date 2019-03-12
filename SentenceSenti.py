import pandas as pd
import re
import subprocess

def preprocess(sent):
    words = str(sent).split()
    new_words = []
    for w in words:
        # remove non English word characters
        w = re.sub(r'[^\x00-\x7F]+',' ', w).lower()
        #remove digits
        w = re.sub(r'[0-9]+', '', w)  
        w = re.sub(r'_person_', '', w)  
        new_words.append(w)
        
    return ' '.join(new_words)

def getSentence(text, wordlist):
    text = preprocess(text)
    #for word in wordlist:
    if type(text) is str:
        result = [sentence + '.' for sentence in text.split('.') if any(' '+x+' ' in sentence for x in wordlist)]
    else:
        result = 'NULL'
    return result

def SentimentSum(data,colname):
    data[colname] = data['Positive'] + data['Negative']
    data2 = data.iloc[1:]
    data2['post_id'] = data2['Text'].apply(lambda x: x.split(',')[1])
    data3 = data2[['post_id',colname]]
    return data3

path =  '/Users/lucia/phd_work/Clpsy/'
file = pd.read_csv(path + 'data/clpsych19_training_data/Btrain_NoNoise_SW.csv')

print('get sentences')
selfList = ['myself']
partnerList = ['boyfriend','girlfriend','bf','gf','ex','wife','husband','partner','my so']
family = ['mom','dad','parents','father','mother','my sister','my brother','friend','family','friends','grandma','grandmother','grandpa','grandfather']

file['family'] = file.apply(lambda x: getSentence(x['post_body'], family), axis=1)
file['self'] = file.apply(lambda x: getSentence(x['post_body'], selfList), axis=1)
file['partner'] = file.apply(lambda x: getSentence(x['post_body'], partnerList), axis=1)


file[['post_id','family']].to_csv(path + 'suicideDetection/features/sentences/familySen.csv')
file[['post_id','self']].to_csv(path + 'suicideDetection/features/sentences/selfSen.csv')
file[['post_id','partner']].to_csv(path + 'suicideDetection/features/sentences/partner.csv')

print('sentistrength')
cmd = path + "suicideDetection/features/sentences/test.sh"
subprocess.call(cmd, shell =True)

print('sum sentiment')

familySenti = pd.read_csv(path + 'suicideDetection/features/sentences/familySen0_out.txt', sep="\t", header='infer')                                                                 
partnerSenti = pd.read_csv(path + 'suicideDetection/features/sentences/partner0_out.txt', sep="\t", header='infer')
selfSenSenti = pd.read_csv(path + 'suicideDetection/features/sentences/selfSen0_out.txt', sep="\t", header='infer')

familySentiSum = SentimentSum(familySenti, 'family_senti')
partnerSentiSum = SentimentSum(partnerSenti, 'partner_senti')
selfSenSum = SentimentSum(selfSenSenti, 'self_senti')

TopicSenti = pd.merge(familySentiSum,partnerSentiSum, on ='post_id')
TopicSenti = pd.merge(TopicSenti,selfSenSum, on ='post_id')

TopicSenti.to_csv(path + 'suicideDetection/features/topicSentiment.csv')






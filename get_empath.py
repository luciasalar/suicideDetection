from empath import Empath
import pandas as pd
import json

class GetEmpath:

    def __init__(self, path, tweetFile):
        """define the main path"""
        self.path = path
        self.tweets = pd.read_csv(self.path + tweetFile)


    def convert_dict(self):
        """Convert to dictionary """

        tweet_dict = {}

        for tweetid, tweet in zip(self.tweets['tweet_id'], self.tweets['text']):
            tweet_dict[tweetid] = tweet

        return tweet_dict

    def get_empath(self, empathCol):
        """Get empath score """

        tweet_dict = self.convert_dict()
        lexicon = Empath()

        empath_dict = {}
        for tweetid, tweet in tweet_dict.items():

            result = lexicon.analyze(tweet, normalize=True)
            empath_dict[tweet] = result[empathCol]

        with open(self.path + 'empath.json', 'a') as f:
                json.dump(empath_dict, f)

        # empath_df = pd.DataFrame.from_dict(data, orient='index')
        # empath_df['tweet_id'] = empath_df.index
        # empath_df.columns = [empathCol, 'tweet_id']

        return empath_dict


path = '/afs/inf.ed.ac.uk/user/s16/s1690903/share/suicide_detection2021/clpsych2021-shared-task/practice-dataset/'
tweetFile = 'tweets_practice.csv' 


em = GetEmpath(path=path, tweetFile=tweetFile)
empath_df = em.get_empath('friends')





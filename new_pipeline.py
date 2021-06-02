from merge_features_2019 import *
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer,TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.metrics import confusion_matrix, f1_score, precision_score,\
recall_score, confusion_matrix, classification_report, accuracy_score 
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_selection import SelectFromModel
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report
from sklearn.impute import SimpleImputer, MissingIndicator
from ruamel import yaml
import sklearn
import time
import gc
import datetime




def load_experiment(path_to_experiment):
    #load experiment 
    data = yaml.safe_load(open(path_to_experiment))
    return data

class PrepareData:
    def __init__(self, feature_path, data_path, merge):
        '''define the main path'''
        self.data_path = data_path
        self.feature_path = feature_path
    
        self.merge = merge

    def features_labels(self):
        """Get all features and labels"""

        all_features = self.merge.merge_features()

        labels = self.tweetFile[['user_id', 'raw_label']]

        features_labels = new_l.merge(all_features, on='user_id', how='inner')

        features_labels.to_csv(self.path + 'temp2.csv')

        return features_labels



    def pre_train(self):
        '''merge data, get X, y and recode y '''

        features = self.merge.merge_features()
      
        # drop label in feature table
        X = features.drop(columns=['raw_label'])
        y = features['raw_label']

        return X, y

    def get_train_test_split(self):
        '''split 10% holdout set, then split train test with the rest 90%, stratify splitting'''
        X, y = self.pre_train()
        # get 10% holdout set for testing
        # X_train1, X_final_test, y_train1, y_final_test = train_test_split(X, y, test_size=0.10, random_state = 2020, stratify = y)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state = 300, stratify = y)
        # split train test in the rest of 90% 
        # X_train, X_test, y_train, y_test = train_test_split(X_train1, y_train1, test_size=0.30, random_state = 2020, stratify = y_train1)

        return X_train, X_test, y_train, y_test


class ColumnSelector(BaseEstimator, TransformerMixin):
    '''feature selector for pipline (pandas df format) '''
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        assert isinstance(X, pd.DataFrame)

        try:
            return X[self.columns]
        except KeyError:
            cols_error = list(set(self.columns) - set(X.columns))
            raise KeyError("The DataFrame does not include the columns: %s" % cols_error)

    def get_feature_names(self):
        return self.columns.tolist
            


class TrainingClassifiers: 
    
    def __init__(self, X_train, X_test, y_train, y_test, parameters, feature_list, feature_set, tfidf_words, classifier, path):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.parameters = parameters
        self.features_list = feature_list
        self.feature_set = feature_set
        self.tfidf_words = tfidf_words
        self.classifier = classifier
        self.path = path

    def select_features(self):
        '''
        select columns with names in feature list then convert it to a transformer object 
        features_list is in the dictionary
        '''
        fea_list = []
        for fea in self.features_list:# select column names with keywords in dict
            f_list = [i for i in self.X_train.columns if fea in i]
            fea_list.append(f_list)
        # flatten a list
        flat = [x for sublist in fea_list for x in sublist]
        # convert to transformer object
        # selected_features = FunctionTransformer(lambda x: x[flat], validate=False)

        return flat

    def get_other_feature_names(self):
        fea_list = []
        for fea in self.features_list: # select column names with keywords in dict
            f_list = [i for i in self.X_train.columns if fea in i]
            fea_list.append(f_list)
        #flatten a list
        flat = [x for sublist in fea_list for x in sublist]
        #convert to transformer object
        return flat


    def setup_pipeline(self):
        '''set up pipeline'''
        features_col = self.get_other_feature_names()

        pipeline = Pipeline([
        # ColumnSelector(columns = features_list),
            
            ('feats', FeatureUnion([
        # generate count vect features
                ('text', Pipeline([

                    ('selector', ColumnSelector(columns='post_body')),
                    # ('cv', CountVectorizer()),
                    ('tfidf', TfidfVectorizer(max_features=self.tfidf_words, ngram_range = (1,3), stop_words ='english', max_df = 0.50, min_df = 0.0025)),
                    # ('svd', TruncatedSVD(algorithm='randomized', n_components=300))
                     ])),
          # # select other features, feature sets are defines in the yaml file

                ('other_features', Pipeline([

                    ('selector', ColumnSelector(columns=features_col)),
                    ('impute', SimpleImputer(strategy='mean')), # impute nan with mean
                ])),

             ])),


               ('clf', Pipeline([
               # ('impute', SimpleImputer(strategy='mean')), #impute nan with mean
               ('scale', StandardScaler(with_mean=False)),  # scale features
                ('classifier', eval(self.classifier)()),  # classifier
           
                 ])),
        ])
        return pipeline

    

    def training_models(self, pipeline):
        '''train models with grid search'''
        grid_search_item = GridSearchCV(pipeline, self.parameters, cv=5, scoring='accuracy')
        grid_search = grid_search_item.fit(self.X_train, self.y_train)
        
        return grid_search

    def test_model(self, path, classifier):
        '''test model and save data'''
        start = time.time()
        #training model
        print('getting pipeline...')
        #the dictionary returns a list, here we extract the string from list use [0]
        pipeline = self.setup_pipeline()

        print('features', self.features_list)
        grid_search = self.training_models(pipeline)
        #make prediction
        print('prediction...')
      
        y_true, y_pred = self.y_test, grid_search.predict(self.X_test)
        report = classification_report(y_true, y_pred, output_dict=True)
        #store prediction result
        y_pred_series = pd.DataFrame(y_pred)
        result = pd.concat([pd.Series(y_true).reset_index(drop=True), y_pred_series], axis = 1)
        result.columns = ['y_true', 'y_pred']
        # test_id = pd.read_csv(path + 'test_feature.csv')
        # result['userid'] = test_id['userid']
        result.to_csv(self.path + 'results/best_result_{}.csv'.format(self.feature_set) )
        end = time.time()
        print('running time:{}'.format(end - start))

        return report, grid_search, pipeline


def loop_the_grid_train_only(feature_path, data_path, env_path, results_path, merge):
    '''loop parameters in the environment file '''

    experiment = load_experiment(env_path + 'experiment.yaml')

    file_exists = os.path.isfile(results_path + 'results/stratify_test_{}.csv'.format(outputname))
    f = open(results_path + 'results/stratify_test_{}.csv'.format(outputname), 'a')
    writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    if not file_exists:
        writer_top.writerow(['best_scores'] + ['best_parameters'] + ['report'] + ['time'] + ['model'] +['feature_set'] +['tfidf_words'])
        f.close()

    for classifier in experiment['experiment']:
        print('classifer is:', classifier)
       
        # prepare environment
        #prepare = PrepareData(timewindow=timewindow, step=step)
        prepare = PrepareData(feature_path = feature_path, data_path = data_path, merge=merge)
        
        # split data
        X_train, X_test, y_train, y_test = prepare.get_train_test_split()
        X_train.to_csv(results_path + 'train_feature.csv')
        X_test.to_csv(results_path + 'test_feature.csv')
        X_train = X_train.drop(columns=['user_id'])
        X_test = X_test.drop(columns=['user_id'])

        # loop feature set
        for feature_set, features_list in experiment['features'].items(): #loop feature sets
            for tfidf_words in experiment['tfidf_features']['max_fea']: #loop tfidf features

                f = open(results_path + 'results/stratify_test_{}.csv'.format(outputname) , 'a')
                writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

                parameters = experiment['experiment'][classifier]
                print('parameters are:', parameters)

                training = TrainingClassifiers(X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test, parameters=parameters, feature_list = features_list, feature_set=feature_set, tfidf_words=tfidf_words, classifier=classifier, path= results_path)

                print('initiate training...')

                report, grid_search, pipeline = training.test_model(path=results_path, classifier=classifier)

                print(report)

                result_row = [[grid_search.best_score_, grid_search.best_params_, pd.DataFrame(report).round(3), str(datetime.datetime.now()), classifier, features_list, tfidf_words]]

                writer_top.writerows(result_row)

                f.close()
                gc.collect()




data_path = '/disk/data/share/s1690903/shareTask/data/clpsych19_training_data/'
feature_path = '/disk/data/share/s1690903/shareTask/suicideDetection/features/'
results_path = '/disk/data/share/s1690903/shareTask/'
env_path = '/disk/data/share/s1690903/shareTask/evn/'


### parameters for training

#experiment = load_experiment(script_path + 'experiment.yaml')
#parameters = experiment['experiment']['sklearn.linear_model.LogisticRegression']
#features_list = experiment['features']['set2']
#tfidf_words = 2000
#classifier = 'sklearn.linear_model.LogisticRegression'
outputname = 'tfidf300'

merge = MergeFeatures(feature_path = feature_path, data_path = data_path)                    
loop_the_grid_train_only(feature_path = feature_path, data_path = data_path, env_path = env_path, results_path=results_path, merge=merge)


# p = PrepareData(timewindow=timewindow, tweetFile=tweetFile, path=data_path, liwcFile=liwcFile, SentimentFile=SentimentFile, mood_step=mood_step, mood_gap=mood_gap, categories=categories, liwc_gap=liwc_gap)
# fl = p.features_labels()
# X_train, X_test, y_train, y_test = p.get_train_test_split()

# train = TrainingClassifiers(X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test, parameters=parameters, features_list=features_list, tfidf_words=tfidf_words, classifier=classifier, path= data_path)

# #pipeline = train.setup_pipeline()
# #grid_search = train.training_models(pipeline)
# report, grid_search, pipeline = train.test_model(path=data_path, classifier=classifier)







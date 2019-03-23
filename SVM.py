import pandas as pd
import numpy as np

from sklearn.datasets import make_classification
from sklearn.metrics import confusion_matrix, f1_score, precision_score,\
recall_score, confusion_matrix, classification_report, accuracy_score 
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold
from sklearn.linear_model import SGDClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.svm import LinearSVC
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sys import argv
import gc
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline
from imblearn.pipeline import make_pipeline, Pipeline
from imblearn.combine import SMOTEENN
from sklearn.preprocessing import StandardScaler, Normalizer

from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt

def SGDclassifier(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=30)
    smote_enn = SMOTEENN(random_state=42)
    cv = StratifiedKFold(n_splits=5, random_state = 0)
    clf = make_pipeline(smote_enn, StandardScaler(), SGDClassifier(max_iter= 1000))

    parameters = [{'sgdclassifier__alpha': [0.01, 0.05, 0.001, 0.005], 'sgdclassifier__class_weight':['balanced'],
                  'sgdclassifier__loss': ['hinge','log','modified_huber','squared_hinge', 'perceptron'], 
                   'sgdclassifier__penalty':['none','l1','l2']}]

    grid_search_item = GridSearchCV(clf,
                              param_grid = parameters,
                               scoring = 'accuracy',
                               cv = cv,
                               n_jobs = -1)

    grid_search = grid_search_item.fit(X_train, y_train)

    print('Best scores and best parameters')
    print(grid_search.best_score_)
    print(grid_search.best_params_)

    y_true, y_pred = y_test, grid_search.predict(X_test)
    print(classification_report(y_true, y_pred))
    print(confusion_matrix(y_true, y_pred))


def ImportantFea(X, y):

	model = ExtraTreesClassifier(random_state = 0)
	model.fit(X, y)
	print(model.feature_importances_)

	print("Feature ranking:")

	importances = model.feature_importances_
	std = np.std([tree.feature_importances_ for tree in model.estimators_],
             axis=0)
	indices = np.argsort(importances)[::-1]
	for f in range(X.shape[1]):
		print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

	feat_importances = pd.Series(model.feature_importances_, index=X.columns)
	feat_importances.nlargest(20).plot(kind='barh')
	plt.show()

	fea_df = pd.DataFrame(feat_importances)
	fea_df['features'] = fea_df.index
	fea_df.columns = ['importance','features']
	fea_df.to_csv(path + 'topFea.csv')
	return fea_df

def selectFea(FeaImportant, Nfea):
    sortFea = FeaImportant.sort_values(by=['importance'],ascending=False)
    select = sortFea[1:Nfea]   
    return select.features.values


def SVMclassifier(X, y):

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=35)

	smote_enn = SMOTEENN(random_state=42)
	cv = StratifiedKFold(n_splits=5, random_state = 0)
	svc = make_pipeline(smote_enn, StandardScaler(), svm.SVC())
	parameters = [{'svc__kernel': ['linear', 'poly', 'rbf', 'sigmoid'], 'svc__gamma': [0.01, 0.001, 0.0001],
	                     'svc__C':[0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 1.5, 2.0, 10] , 'svc__class_weight':['balanced']}]
	                   
	grid_search_item = GridSearchCV(estimator = svc,
	                          param_grid = parameters,
	                           cv =  cv,
	                           scoring = 'accuracy',
	                           n_jobs = -1)
	grid_search = grid_search_item.fit(X_train, y_train)

	print('Best scores and best parameters')
	print(grid_search.best_score_)
	print(grid_search.best_params_)

	y_true, y_pred = y_test, grid_search.predict(X_test)
	print(classification_report(y_true, y_pred))


def GetLIWC(file:str): 
	liwc = pd.read_csv(file)
	liwc = liwc.rename(columns = {liwc.columns[2]:'user_id'})
	liwcUser = liwc.groupby('user_id').mean().reset_index()
	liwcUser = liwcUser.drop(['Source (A)', 'Source (D)'], axis=1)
	return liwcUser


path = '/Users/lucia/phd_work/Clpsy/'
#path = '/home/lucia/phd_work/shareTask/'
features = pd.read_csv(path + 'suicideDetection/features/FreqSentiMotiTopiFea.csv')

#merge features
liwcUser = GetLIWC(path + 'suicideDetection/features/liwcSW.csv')
liwcUser2 = liwcUser.iloc[:,1::]
liwcUser2.columns = [str(col) + '_liwc' for col in liwcUser2.columns]
liwcUser2['user_id'] = liwcUser.user_id

empath = pd.read_csv(path + 'suicideDetection/features/empathSW.csv')
empath2 = empath.iloc[:,1::]
empath2.columns = [str(col) + '_empath' for col in empath2.columns]
empath2['user_id'] = empath.user_id

allfea = pd.merge(features, liwcUser2, on = 'user_id', how = 'right')
allfea = pd.merge(allfea, empath2, on = 'user_id', how = 'right')

#select features and split train test
X = allfea.iloc[:, 3:146]
y = allfea.raw_label


##add count vect
text = pd.read_csv(path + 'data/clpsych19_training_data/Btrain_NoNoise_SW.csv')
countVect = pd.read_csv(path + 'countVec2.csv')
countVect['user_id'] = text['user_id']
countVec2 = countVect.groupby(['user_id']).mean().reset_index()

#add tfidf count vect as features
allfea = pd.merge(allfea, countVec2, on = 'user_id', how = 'right')
#X = allfea.iloc[:, 3::]
y = allfea.raw_label
allfea2 = allfea.iloc[:, 1::]
allfea2 = allfea2.drop(['raw_label'],axis = 1)
feaImp = ImportantFea(allfea2, y)
#select top N features 
selectFea = selectFea(feaImp,200)

selectedFea = allfea2.loc[:, allfea2.columns.isin(selectFea)]
selectedFea['user_id'] = allfea2.user_id

#SVMclassifier(selectedFea,y)

print (liwcUser2.head(5))


#allfea.to_csv(path + 'allFea.csv')




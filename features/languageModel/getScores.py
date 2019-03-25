def getClass(file, Class, savePath):
    a = file.loc[file['raw_label_x'] == Class]
    a = a[['post_body','post_title']]
    a.to_csv(savePath)
    

savePath1 = path + 'data/languageModel/AAll.csv'
savePath2 = path + 'data/languageModel/BAll.csv'
savePath3 = path + 'data/languageModel/CAll.csv'
savePath4 = path + 'data/languageModel/DAll.csv'

ClassA = getClass(allPtrain, 'a', savePath1)
ClassB = getClass(allPtrain, 'b', savePath2)
ClassC = getClass(allPtrain, 'c', savePath3)
ClassD = getClass(allPtrain, 'd', savePath4)
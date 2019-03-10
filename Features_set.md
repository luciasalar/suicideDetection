# Features set:
## Similarity of postng behaviour 
This set concerns with capturing the user posting behaviour as sign of similarity between the users. 
* Subredit_vec: Vector of the subreddits the user posted at. This set of feature will be represented as counter vectorizer. 

* Sentiment in posting: compute the similarity between users sentiment profile. Vector of sentiment in posting [p1_neg, p2_pos, ..etc]. Another representatin is to use the edit distance between two vector and calculate the mean of the edit for each user. 

##Frequency:
* Frequency_of_posting: mean average time between two supsequent posts, number of posts, average number of words in each posts, whether user is posting more frequent. This method is applied on general posts, SW posts and posts that mention mental health, drug issues, addiction and health issues (file: features/FreFea.csv  n = 496, without control group) 


##Post content:
* LIWC of SW posts (N = 919 (post level), no control group): this is the LIWC features for SW posts only (file: features/liwcSW.csv)

* LIWC of non-SW posts (N = 919 (post level), no control group): this is the LIWC features for non-SW posts only (file: features/liwcNoSW.csv)

* empath of SW posts (N = 496 (user level), no control group): this is the empath features for SW posts only (file: features/empathSW.csv)

* part-of-speech taggings of SW posts (N = 496 (user level), no control group): this is the part-of-speech tagging for SW posts only 

number of tags in the posts is normalized by word count of the posts. nouns(NN), plural nouns (NNS), comparative words (JJR), modal (MD), proper nound (NNP), plural proper (NNPS), predeterminer (PDT), possessive ending(POS), personal pronoun (PRP), possessive pronoun(PRP$), verbs (VB) (VBD) (VBG) (VBN) (VBZ). 

## motivations:
* we summarise a few suicide motivation: financial problems, drug and drinking, mental health, relationship problem suicide methods. Each motivation is corresponded with a dictionary. We check whether post body cantain these words. Then we aggregate the number of suicide motivation for each user (features/motivations.csv) 

features/feaCor2.csv shows the correlations between motivation var, freq var and the labels






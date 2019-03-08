# Features set:
## Similarity of postng behaviour 
This set concerns with capturing the user posting behaviour as sign of similarity between the users. 
* Subredit_vec: Vector of the subreddits the user posted at. This set of feature will be represented as counter vectorizer. 
* Frequency_of_posting: mean average time between last two supsequent posts. 
* Sentiment in posting: compute the similarity between users sentiment profile. Vector of sentiment in posting [p1_neg, p2_pos, ..etc]. Another representatin is to use the edit distance between two vector and calculate the mean of the edit for each user. 
* part-of-speech taggings: part-of-speech taggings of SW posts: number of tags in the posts normalized by  nouns(NN), plural nouns (NNS), comparative words (JJR), modal (MD), proper nound (NNP), plural proper (NNPS), predeterminer (PDT), possessive ending(POS), personal pronoun (PRP), possessive pronoun(PRP$), verbs (VB) (VBD) (VBG) (VBN) (VBZ), 
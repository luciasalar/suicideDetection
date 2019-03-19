The language model is a 5gram modified Kneser-Nay

OOV - number of out of vocabulary words in the test file
PPL_NO_OOV -> Perplexity score excluding out of vocabulary words (lower is better)
PPL_OOV -> Perplexity with out of vocabulary words (lower is better)



there's two variants of those files. One is a language model trained on the raw (ish) text, the other one is a language model trained on a truecased and tokenized text (which is standard practise)

raw oov:
 precision    recall  f1-score   support

           a       0.84      0.70      0.76        92
           b       0.73      1.00      0.84        16
           c       0.35      1.00      0.51        19
           d       0.83      0.65      0.73       121

   micro avg       0.72      0.72      0.72       248
   macro avg       0.69      0.84      0.71       248
weighted avg       0.79      0.72      0.73       248


ppl_no_oov:
              precision    recall  f1-score   support

           a       0.59      1.00      0.74        45
           b       0.73      0.80      0.76        20
           c       0.55      0.48      0.51        63
           d       0.83      0.66      0.73       120

   micro avg       0.69      0.69      0.69       248
   macro avg       0.67      0.73      0.69       248
weighted avg       0.71      0.69      0.68       248


ppl_oov:
              precision    recall  f1-score   support

           a       0.71      0.92      0.80        59
           b       0.73      1.00      0.84        16
           c       0.36      0.87      0.51        23
           d       0.97      0.61      0.75       150

   micro avg       0.73      0.73      0.73       248
   macro avg       0.69      0.85      0.73       248
weighted avg       0.84      0.73      0.75       248


tc_tok:

              precision    recall  f1-score   support

           a       0.79      0.61      0.69        99
           b       0.73      1.00      0.84        16
           c       0.35      1.00      0.51        19
           d       0.80      0.67      0.73       114

   micro avg       0.69      0.69      0.69       248
   macro avg       0.67      0.82      0.69       248
weighted avg       0.76      0.69      0.70       248

tc_tok ppl_no_oov:
              precision    recall  f1-score   support

           a       0.59      0.92      0.72        49
           b       0.73      0.80      0.76        20
           c       0.45      0.60      0.52        42
           d       0.93      0.64      0.76       137

   micro avg       0.70      0.70      0.70       248
   macro avg       0.68      0.74      0.69       248
weighted avg       0.76      0.70      0.71       248

tc_tok ppl_oov
              precision    recall  f1-score   support

           a       0.72      0.86      0.79        64
           b       0.73      1.00      0.84        16
           c       0.35      0.95      0.51        20
           d       0.97      0.62      0.76       148

   micro avg       0.73      0.73      0.73       248
   macro avg       0.69      0.86      0.72       248
weighted avg       0.84      0.73      0.75       248

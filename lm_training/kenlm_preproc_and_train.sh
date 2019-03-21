#!/bin/bash
export KENLM_BUILD_PATH=/home/dheart/uni_stuff/postdoc/suidet/kenlm/build
export NGRAM_ORDER=5

export root_path=$1
export csv_file_path=$2

export Train=$root_path/Train
export test_all_a=$root_path/test_all_a
export test_all_b=$root_path/test_all_b
export test_all_c=$root_path/test_all_c
export test_all_d=$root_path/test_all_d
export models=$root_path/models
export arpas=$root_path/arpas
export scores=$root_path/scores

#for BPE:
export BPE_HOME=./fastBPE
export bpe_merges=15000
export moses_scripts=./moses-scripts/scripts
export bpe_file=$models/en.15k.bpe
export vocab=$models/vocab.en.15k
export tc_model=$models/truecase-model.en


#split and preprocess
mkdir -p $Train
mkdir -p $test_all_a
mkdir -p $test_all_b
mkdir -p $test_all_c
mkdir -p $test_all_d
mkdir -p $models
mkdir -p $arpas/rawish
mkdir -p $arpas/tok_tc
mkdir -p $scores/{rawish,tok_tc}/{oov,ppl_no_oov,ppl_oov}/{test_all_a,test_all_b,test_all_c,test_all_d}

#Clean up directories

rm -rf $Train/*
rm -rf $test_all_a/*
rm -rf $test_all_b/*
rm -rf $test_all_c/*
rm -rf $test_all_d/*


python3 preproc.py $csv_file_path All.csv $Train "$csv_file_path/allPtest.csv" $root_path/test_all

#Tokenize, truecase and BPE functions
tok_tc_bpe_apply_test () {
	#Tok and punctuation
	$moses_scripts/tokenizer/normalize-punctuation.perl -l en < $1 | $moses_scripts/tokenizer/tokenizer.perl -a -l en > $1.tok

	#apply TC
	$moses_scripts/recaser/truecase.perl -model $tc_model < $1.tok > $1.tok.tc

	#apply bpe
	$BPE_HOME/fast applybpe $1.bpe $1.tok.tc $bpe_file $vocab
}

tok_tc_bpe_train () {
	#Tok and punctuation
	$moses_scripts/tokenizer/normalize-punctuation.perl -l en < $1 | $moses_scripts/tokenizer/tokenizer.perl -a -l en > $1.tok

	#truecase
	$moses_scripts/recaser/train-truecaser.perl -corpus $1.tok -model $tc_model

	#apply TC
	$moses_scripts/recaser/truecase.perl -model $tc_model < $1.tok > $1.tok.tc

	#train BPE
	$BPE_HOME/fast learnbpe $bpe_merges $1.tok.tc > $bpe_file

	#apply bpe
	$BPE_HOME/fast applybpe $1.bpe $1.tok.tc $bpe_file #$vocab for test

	#Get vocab:
	$BPE_HOME/fast getvocab $1.bpe > $vocab
}

cat $Train/*.txt > $Train/all.txt

tok_tc_bpe_train $Train/all.txt
tok_tc_bpe_apply_test $Train/A.txt
tok_tc_bpe_apply_test $Train/B.txt
tok_tc_bpe_apply_test $Train/C.txt
tok_tc_bpe_apply_test $Train/D.txt

for filename in $test_all_a/*; do
	tok_tc_bpe_apply_test $filename
done

for filename in $test_all_b/*; do
	tok_tc_bpe_apply_test $filename
done

for filename in $test_all_c/*; do
	tok_tc_bpe_apply_test $filename
done

for filename in $test_all_d/*; do
	tok_tc_bpe_apply_test $filename
done

#Train KenLM now
$KENLM_BUILD_PATH/bin/lmplz -o $NGRAM_ORDER < $Train/A.txt > $arpas/rawish/A.arpa
$KENLM_BUILD_PATH/bin/build_binary $arpas/rawish/A.arpa $arpas/rawish/A.binlm
$KENLM_BUILD_PATH/bin/lmplz -o $NGRAM_ORDER < $Train/A.txt.tok.tc > $arpas/tok_tc/A.tok.tc.arpa
$KENLM_BUILD_PATH/bin/build_binary $arpas/tok_tc/A.tok.tc.arpa $arpas/tok_tc/A.tok.tc.binlm

$KENLM_BUILD_PATH/bin/lmplz -o $NGRAM_ORDER < $Train/B.txt > $arpas/rawish/B.arpa
$KENLM_BUILD_PATH/bin/build_binary $arpas/rawish/B.arpa $arpas/rawish/B.binlm
$KENLM_BUILD_PATH/bin/lmplz -o $NGRAM_ORDER < $Train/B.txt.tok.tc > $arpas/tok_tc/B.tok.tc.arpa
$KENLM_BUILD_PATH/bin/build_binary $arpas/tok_tc/B.tok.tc.arpa $arpas/tok_tc/B.tok.tc.binlm

$KENLM_BUILD_PATH/bin/lmplz -o $NGRAM_ORDER < $Train/C.txt > $arpas/rawish/C.arpa
$KENLM_BUILD_PATH/bin/build_binary $arpas/rawish/C.arpa $arpas/rawish/C.binlm
$KENLM_BUILD_PATH/bin/lmplz -o $NGRAM_ORDER < $Train/C.txt.tok.tc > $arpas/tok_tc/C.tok.tc.arpa
$KENLM_BUILD_PATH/bin/build_binary $arpas/tok_tc/C.tok.tc.arpa $arpas/tok_tc/C.tok.tc.binlm

$KENLM_BUILD_PATH/bin/lmplz -o $NGRAM_ORDER < $Train/D.txt > $arpas/rawish/D.arpa
$KENLM_BUILD_PATH/bin/build_binary $arpas/rawish/D.arpa $arpas/rawish/D.binlm
$KENLM_BUILD_PATH/bin/lmplz -o $NGRAM_ORDER < $Train/D.txt.tok.tc > $arpas/tok_tc/D.tok.tc.arpa
$KENLM_BUILD_PATH/bin/build_binary $arpas/tok_tc/D.tok.tc.arpa $arpas/tok_tc/D.tok.tc.binlm

#Evaluate

score_kenlm () {
	export kenlm_query="$KENLM_BUILD_PATH/bin/query"

	export SCORES_A="$1/A.binlm"

	export SCORES_B="$1/B.binlm"

	export SCORES_C="$1/C.binlm"

	export SCORES_D="$1/D.binlm"

	for filename in $2/*; do

		base_filename=$(basename $filename)

		if [[ $filename == *.* ]]; then
	  		continue #ignore .bpe .tok.tc
		fi

	    $kenlm_query $SCORES_A < $filename > /tmp/a_score
	    ppl_oov_a=`grep "Perplexity including OOVs:" /tmp/a_score | sed 's/^.*\(Perplexity including OOVs:\)/\1/'  | awk '{print $4}'`
	    ppl_no_oov_a=`grep "Perplexity excluding OOVs:" /tmp/a_score | sed 's/^.*\(Perplexity excluding OOVs:\)/\1/'  | awk '{print $4}'`
	    oov_a=`grep "OOVs:" /tmp/a_score | tail -n1 | awk '{print $2}'`

	    $kenlm_query $SCORES_B < $filename | tail -n4 > /tmp/b_score
	    ppl_oov_b=`grep "Perplexity including OOVs:" /tmp/b_score | sed 's/^.*\(Perplexity including OOVs:\)/\1/'  | awk '{print $4}'`
	    ppl_no_oov_b=`grep "Perplexity excluding OOVs:" /tmp/b_score | sed 's/^.*\(Perplexity excluding OOVs:\)/\1/'  |  awk '{print $4}'`
	    oov_b=`grep "OOVs:" /tmp/b_score | tail -n1 | awk '{print $2}'`

	    $kenlm_query $SCORES_C < $filename | tail -n4 > /tmp/c_score
	    ppl_oov_c=`grep "Perplexity including OOVs:" /tmp/c_score | sed 's/^.*\(Perplexity including OOVs:\)/\1/'  | awk '{print $4}'`
	    ppl_no_oov_c=`grep "Perplexity excluding OOVs:" /tmp/c_score | sed 's/^.*\(Perplexity excluding OOVs:\)/\1/'  |  awk '{print $4}'`
	    oov_c=`grep "OOVs:" /tmp/c_score | tail -n1 | awk '{print $2}'`

	    $kenlm_query $SCORES_D < $filename | tail -n4 > /tmp/d_score
	    ppl_oov_d=`grep "Perplexity including OOVs:" /tmp/d_score | sed 's/^.*\(Perplexity including OOVs:\)/\1/'  | awk '{print $4}'`
	    ppl_no_oov_d=`grep "Perplexity excluding OOVs:" /tmp/d_score | sed 's/^.*\(Perplexity excluding OOVs:\)/\1/'  |  awk '{print $4}'`
	    oov_d=`grep "OOVs:" /tmp/d_score | tail -n1 | awk '{print $2}'`

	    echo $ppl_oov_a $ppl_oov_b $ppl_oov_c $ppl_oov_d > $3/ppl_oov/$4/$base_filename.scores
	    echo $ppl_no_oov_a $ppl_no_oov_b $ppl_no_oov_c $ppl_no_oov_d > $3/ppl_no_oov/$4/$base_filename.scores
	    echo $oov_a $oov_b $oov_c $oov_d > $3/oov/$4/$base_filename.scores
	done
}

score_kenlm_tok_tc () {
	export kenlm_query="$KENLM_BUILD_PATH/bin/query"

	export SCORES_A="$1/A.tok.tc.binlm"

	export SCORES_B="$1/B.tok.tc.binlm"

	export SCORES_C="$1/C.tok.tc.binlm"

	export SCORES_D="$1/D.tok.tc.binlm"

	for filename in $2/*.tok.tc; do

		base_filename=$(basename $filename)

	    $kenlm_query $SCORES_A < $filename > /tmp/a_score
	    ppl_oov_a=`grep "Perplexity including OOVs:" /tmp/a_score | sed 's/^.*\(Perplexity including OOVs:\)/\1/'  | awk '{print $4}'`
	    ppl_no_oov_a=`grep "Perplexity excluding OOVs:" /tmp/a_score | sed 's/^.*\(Perplexity excluding OOVs:\)/\1/'  | awk '{print $4}'`
	    oov_a=`grep "OOVs:" /tmp/a_score | tail -n1 | awk '{print $2}'`

	    $kenlm_query $SCORES_B < $filename | tail -n4 > /tmp/b_score
	    ppl_oov_b=`grep "Perplexity including OOVs:" /tmp/b_score | sed 's/^.*\(Perplexity including OOVs:\)/\1/'  | awk '{print $4}'`
	    ppl_no_oov_b=`grep "Perplexity excluding OOVs:" /tmp/b_score | sed 's/^.*\(Perplexity excluding OOVs:\)/\1/'  |  awk '{print $4}'`
	    oov_b=`grep "OOVs:" /tmp/b_score | tail -n1 | awk '{print $2}'`

	    $kenlm_query $SCORES_C < $filename | tail -n4 > /tmp/c_score
	    ppl_oov_c=`grep "Perplexity including OOVs:" /tmp/c_score | sed 's/^.*\(Perplexity including OOVs:\)/\1/'  | awk '{print $4}'`
	    ppl_no_oov_c=`grep "Perplexity excluding OOVs:" /tmp/c_score | sed 's/^.*\(Perplexity excluding OOVs:\)/\1/'  |  awk '{print $4}'`
	    oov_c=`grep "OOVs:" /tmp/c_score | tail -n1 | awk '{print $2}'`

	    $kenlm_query $SCORES_D < $filename | tail -n4 > /tmp/d_score
	    ppl_oov_d=`grep "Perplexity including OOVs:" /tmp/d_score | sed 's/^.*\(Perplexity including OOVs:\)/\1/'  | awk '{print $4}'`
	    ppl_no_oov_d=`grep "Perplexity excluding OOVs:" /tmp/d_score | sed 's/^.*\(Perplexity excluding OOVs:\)/\1/'  |  awk '{print $4}'`
	    oov_d=`grep "OOVs:" /tmp/d_score | tail -n1 | awk '{print $2}'`

	    echo $ppl_oov_a $ppl_oov_b $ppl_oov_c $ppl_oov_d > $3/ppl_oov/$4/$base_filename.scores
	    echo $ppl_no_oov_a $ppl_no_oov_b $ppl_no_oov_c $ppl_no_oov_d > $3/ppl_no_oov/$4/$base_filename.scores
	    echo $oov_a $oov_b $oov_c $oov_d > $3/oov/$4/$base_filename.scores
	done
}

score_kenlm $arpas/rawish/ $test_all_a $scores/rawish test_all_a
score_kenlm $arpas/rawish/ $test_all_b $scores/rawish test_all_b
score_kenlm $arpas/rawish/ $test_all_c $scores/rawish test_all_c
score_kenlm $arpas/rawish/ $test_all_d $scores/rawish test_all_d

score_kenlm_tok_tc $arpas/tok_tc/ $test_all_a $scores/tok_tc test_all_a
score_kenlm_tok_tc $arpas/tok_tc/ $test_all_b $scores/tok_tc test_all_b
score_kenlm_tok_tc $arpas/tok_tc/ $test_all_c $scores/tok_tc test_all_c
score_kenlm_tok_tc $arpas/tok_tc/ $test_all_d $scores/tok_tc test_all_d

#Print results
echo "Rawish scores oov for classes A, B, C, D"
echo `python3 evaluate_kenlm.py $scores/rawish/oov/test_all_a`
echo `python3 evaluate_kenlm.py $scores/rawish/oov/test_all_b`
echo `python3 evaluate_kenlm.py $scores/rawish/oov/test_all_c`
echo `python3 evaluate_kenlm.py $scores/rawish/oov/test_all_d`

echo "Rawish scores ppl_oov for classes A, B, C, D"
echo `python3 evaluate_kenlm.py $scores/rawish/ppl_oov/test_all_a`
echo `python3 evaluate_kenlm.py $scores/rawish/ppl_oov/test_all_b`
echo `python3 evaluate_kenlm.py $scores/rawish/ppl_oov/test_all_c`
echo `python3 evaluate_kenlm.py $scores/rawish/ppl_oov/test_all_d`

echo "Rawish scores ppl_no_oov for classes A, B, C, D"
echo `python3 evaluate_kenlm.py $scores/rawish/ppl_no_oov/test_all_a`
echo `python3 evaluate_kenlm.py $scores/rawish/ppl_no_oov/test_all_b`
echo `python3 evaluate_kenlm.py $scores/rawish/ppl_no_oov/test_all_c`
echo `python3 evaluate_kenlm.py $scores/rawish/ppl_no_oov/test_all_d`

echo "Tok.tc scores oov for classes A, B, C, D"
echo `python3 evaluate_kenlm.py $scores/tok_tc/oov/test_all_a`
echo `python3 evaluate_kenlm.py $scores/tok_tc/oov/test_all_b`
echo `python3 evaluate_kenlm.py $scores/tok_tc/oov/test_all_c`
echo `python3 evaluate_kenlm.py $scores/tok_tc/oov/test_all_d`

echo "Tok.tc scores ppl_oov for classes A, B, C, D"
echo `python3 evaluate_kenlm.py $scores/tok_tc/ppl_oov/test_all_a`
echo `python3 evaluate_kenlm.py $scores/tok_tc/ppl_oov/test_all_b`
echo `python3 evaluate_kenlm.py $scores/tok_tc/ppl_oov/test_all_c`
echo `python3 evaluate_kenlm.py $scores/tok_tc/ppl_oov/test_all_d`

echo "Tok.tc scores ppl_no_oov for classes A, B, C, D"
echo `python3 evaluate_kenlm.py $scores/tok_tc/ppl_no_oov/test_all_a`
echo `python3 evaluate_kenlm.py $scores/tok_tc/ppl_no_oov/test_all_b`
echo `python3 evaluate_kenlm.py $scores/tok_tc/ppl_no_oov/test_all_c`
echo `python3 evaluate_kenlm.py $scores/tok_tc/ppl_no_oov/test_all_d`

#Produce reports
python3 to_csv_kenlm.py $scores/rawish/oov/ $root_path/rawish_oov.csv
python3 to_csv_kenlm.py $scores/rawish/ppl_oov/ $root_path/rawish_ppl_oov.csv
python3 to_csv_kenlm.py $scores/rawish/ppl_no_oov/ $root_path/rawish_ppl_no_oov.csv

python3 to_csv_kenlm.py $scores/tok_tc/oov/ $root_path/tok_tc_oov.csv
python3 to_csv_kenlm.py $scores/tok_tc/ppl_oov/ $root_path/tok_tc_ppl_oov.csv
python3 to_csv_kenlm.py $scores/tok_tc/ppl_no_oov/ $root_path/tok_tc_ppl_no_oov.csv

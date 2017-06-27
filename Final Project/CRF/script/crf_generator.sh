#! /bin/bash

template=$1
result=$2
evaluation=$3
model=$4

crf_learn $template word_lemma_pos_iob_train.txt $model
crf_test -m $model word_lemma_pos_iob_test.txt > $result
perl conlleval.pl -d '\t' < $result > $evaluation

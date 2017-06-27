#! /bin/bash

##############################################################################################
#
# @param: ngram order
# @param: smoothing method
#
#########################################################################################################

fstcompile --isymbols=lexicon_lemmaIOB.txt --osymbols=lexicon_lemmaIOB.txt lemma_IOB.txt > lemma_IOB.fst
./elaborator.sh $1 $2

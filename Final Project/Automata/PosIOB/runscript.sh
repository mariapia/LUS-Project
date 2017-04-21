#! /bin/bash

###########################################################################################
#
# @param: ngram order
# @param: smoothing method
#
###########################################################################################

fstcompile --isymbols=lexicon_POSIOB.txt --osymbols=lexicon_POSIOB.txt pos_iob.txt > pos_iob.fst
./elaborator.sh $1 $2

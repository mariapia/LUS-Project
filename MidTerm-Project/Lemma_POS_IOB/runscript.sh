#! /bin/bash

#####################################################################################
#
# @param: ngram order
# @param: smoothing method
#
####################################################################################

./lemmapos_iob.py
fstcompile --isymbols=lexicon.txt --osymbols=lexicon.txt lemmapos_iob.txt > lemmapos_iob.fst
./elaborator.sh $1 $2

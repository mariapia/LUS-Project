#! /bin/bash

./Independent_features.py

fstcompile --isymbols=lexicon.txt --osymbols=lexicon.txt word_lemma.txt > word_lemma.fst
fstcompile --isymbols=lexicon.txt --osymbols=lexicon.txt lemma_pos.txt > lemma_pos.fst
fstcompile --isymbols=lexicon.txt --osymbols=lexicon.txt pos_iob.txt > pos_iob.fst
fstarcsort word_lemma.fst > word_lemma_sort.fst
fstarcsort lemma_pos.fst > lemma_pos_sort.fst
fstarcsort pos_iob.fst > pos_iob_sort.fst

fstcompose word_lemma_sort.fst lemma_pos_sort.fst | fstcompose - pos_iob_sort.fst > global.fst

./elaborator.sh $1 $2

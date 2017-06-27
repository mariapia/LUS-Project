#! /usr/bin/python3

"""
Language Understanding Systems Project
Student: Maria Pia Natale
ID number: 189160

"""

import sys
import math
import random
from collections import Counter

train_file = open("../NLSPARQL.train.data", "r")
train_feat = open("../NLSPARQL.train.feats.txt", "r")
test_file = open("../NLSPARQL.test.data", "r")
test_feat = open("../NLSPARQL.test.feats.txt", "r")

lexicon_lemmapos = open("../lexicon_lemmapos.txt", "w")

train_lemmapos = open("../train_lemmapos", "w")
validation_lemmapos = open("../validation_lemmapos", "w")
test_lemmapos = open("../test_lemmapos", "w")

Seed = 463
random.seed(Seed)
split_f = train_feat.read().split('\n')
split_t = train_file.read().split('\n')


lemma_pos = []
lemma_pos_line = []
lemma_pos_sentences = []

for x,y in zip(split_t, split_f):
    if x != '' and y != '':
        a, b = x.split('\t')  #word iob
        c, d, e = y.split('\t') #word pos lemma
        lemma_pos.append((e, d))
        lemma_pos_line.append((e, d, b))
    else:
        if len(lemma_pos_line) != 0:
            lemma_pos_sentences.append(lemma_pos_line)
            lemma_pos_line = []

split_feat = test_feat.read().split('\n')
split_test = test_file.read().split('\n')


test_data_lemmapos_sentences = []
test_data_lemmapos_line = []

for x,y in zip(split_test, split_feat):
    if x != '' and y != '':
        a, b = x.split('\t')  #word iob
        c, d, e = y.split('\t') #word pos lemma
        test_data_lemmapos_line.append((e, d, b))
    else:
        if len(test_data_lemmapos_line) != 0:
            test_data_lemmapos_sentences.append(test_data_lemmapos_line)
            test_data_lemmapos_line = []

##################################################################################################################
#                                          LEXICON WORD

counted_lemmapos = Counter(lemma_pos)
count = 0

for i in counted_lemmapos:
    lexicon_lemmapos.write(str(i[0]) + "_" + str(i[1]) + "\t" + str(count) + "\n")
    count += 1
lexicon_lemmapos.write("<UNK>\t" + str(count) + "\n")

##################################################################################################################

length_sentences_lemmapos = len(lemma_pos_sentences)
perc = length_sentences_lemmapos * float(sys.argv[1])
random.shuffle(lemma_pos_sentences)

train_data_lemmapos = lemma_pos_sentences[:int(perc)]
validation_data_lemmapos = lemma_pos_sentences[int(perc):]

for i in train_data_lemmapos:
    for x in i:
        train_lemmapos.write(str(x[0]) + "_" + str(x[1]) + "\t" + str(x[2]) + "\n")
    train_lemmapos.write("\n")

for i in validation_data_lemmapos:
    for x in i:
        validation_lemmapos.write(str(x[0]) + "_" + str(x[1]) + "\t" + str(x[2]) + "\n")
    validation_lemmapos.write("\n")


for i in test_data_lemmapos_sentences:
    for x in i:
        test_lemmapos.write(str(x[0]) + "_" + str(x[1]) + "\t" + str(x[2]) + "\n")
    test_lemmapos.write("\n")

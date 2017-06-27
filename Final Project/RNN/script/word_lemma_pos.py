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

lexicon_wordlemmapos = open("../lexicon_wordlemmapos.txt", "w")

train_wordlemmapos = open("../train_wordlemmapos", "w")
validation_wordlemmapos = open("../validation_wordlemmapos", "w")
test_wordlemmapos = open("../test_wordlemmapos", "w")

Seed = 463
random.seed(Seed)
split_f = train_feat.read().split('\n')
split_t = train_file.read().split('\n')


word_lemma_pos = []
word_lemma_pos_line = []
word_lemma_pos_sentences = []

for x,y in zip(split_t, split_f):
    if x != '' and y != '':
        a, b = x.split('\t')  #word iob
        c, d, e = y.split('\t') #word pos lemma
        word_lemma_pos.append((a, e, d))
        word_lemma_pos_line.append((a, e, d, b))
    else:
        if len(word_lemma_pos_line) != 0:
            word_lemma_pos_sentences.append(word_lemma_pos_line)
            word_lemma_pos_line = []

split_feat = test_feat.read().split('\n')
split_test = test_file.read().split('\n')


test_data_wordlemmapos_sentences = []
test_data_wordlemmapos_line = []

for x,y in zip(split_test, split_feat):
    if x != '' and y != '':
        a, b = x.split('\t')  #word iob
        c, d, e = y.split('\t') #word pos lemma
        test_data_wordlemmapos_line.append((a, e, d, b))
    else:
        if len(test_data_wordlemmapos_line) != 0:
            test_data_wordlemmapos_sentences.append(test_data_wordlemmapos_line)
            test_data_wordlemmapos_line = []

##################################################################################################################
#                                          LEXICON WORD

counted_wordlemmapos = Counter(word_lemma_pos)
count = 0

for i in counted_wordlemmapos:
    lexicon_wordlemmapos.write(str(i[0]) + "_" + str(i[1]) + "_" + str(i[2]) + "\t" + str(count) + "\n")
    count += 1
lexicon_wordlemmapos.write("<UNK>\t" + str(count) + "\n")

##################################################################################################################

length_sentences_wordlemmapos = len(word_lemma_pos_sentences)
perc = length_sentences_wordlemmapos * float(sys.argv[1])
random.shuffle(word_lemma_pos_sentences)

train_data_wordlemmapos = word_lemma_pos_sentences[:int(perc)]
validation_data_wordlemmapos = word_lemma_pos_sentences[int(perc):]

for i in train_data_wordlemmapos:
    for x in i:
        train_wordlemmapos.write(str(x[0]) + "_" + str(x[1]) + "_" + str(x[2]) + "\t" + str(x[3]) + "\n")
    train_wordlemmapos.write("\n")

for i in validation_data_wordlemmapos:
    for x in i:
        validation_wordlemmapos.write(str(x[0]) + "_" + str(x[1]) + "_" + str(x[2]) + "\t" + str(x[3]) + "\n")
    validation_wordlemmapos.write("\n")


for i in test_data_wordlemmapos_sentences:
    for x in i:
        test_wordlemmapos.write(str(x[0]) + "_" + str(x[1]) + "_" + str(x[2]) + "\t" + str(x[3]) + "\n")
    test_wordlemmapos.write("\n")

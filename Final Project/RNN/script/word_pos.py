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

lexicon_wordpos = open("../lexicon_wordpos.txt", "w")

train_wordpos = open("../train_wordpos", "w")
validation_wordpos = open("../validation_wordpos", "w")
test_wordpos = open("../test_wordpos", "w")

Seed = 463
random.seed(Seed)
split_f = train_feat.read().split('\n')
split_t = train_file.read().split('\n')


word_pos = []
word_pos_line = []
word_pos_sentences = []

for x,y in zip(split_t, split_f):
    if x != '' and y != '':
        a, b = x.split('\t')  #word iob
        c, d, e = y.split('\t') #word pos lemma
        word_pos.append((a, d))
        word_pos_line.append((a, d, b))
    else:
        if len(word_pos_line) != 0:
            word_pos_sentences.append(word_pos_line)
            word_pos_line = []

split_feat = test_feat.read().split('\n')
split_test = test_file.read().split('\n')


test_data_wordpos_sentences = []
test_data_wordpos_line = []

for x,y in zip(split_test, split_feat):
    if x != '' and y != '':
        a, b = x.split('\t')  #word iob
        c, d, e = y.split('\t') #word pos lemma
        test_data_wordpos_line.append((a, d, b))
    else:
        if len(test_data_wordpos_line) != 0:
            test_data_wordpos_sentences.append(test_data_wordpos_line)
            test_data_wordpos_line = []

##################################################################################################################
#                                          LEXICON WORD

counted_wordpos = Counter(word_pos)
count = 0

for i in counted_wordpos:
    lexicon_wordpos.write(str(i[0]) + "_" + str(i[1]) + "\t" + str(count) + "\n")
    count += 1
lexicon_wordpos.write("<UNK>\t" + str(count) + "\n")

##################################################################################################################

length_sentences_wordpos = len(word_pos_sentences)
perc = length_sentences_wordpos * float(sys.argv[1])
random.shuffle(word_pos_sentences)

train_data_wordpos = word_pos_sentences[:int(perc)]
validation_data_wordpos = word_pos_sentences[int(perc):]

for i in train_data_wordpos:
    for x in i:
        train_wordpos.write(str(x[0]) + "_" + str(x[1]) + "\t" + str(x[2]) + "\n")
    train_wordpos.write("\n")

for i in validation_data_wordpos:
    for x in i:
        validation_wordpos.write(str(x[0]) + "_" + str(x[1]) + "\t" + str(x[2]) + "\n")
    validation_wordpos.write("\n")


for i in test_data_wordpos_sentences:
    for x in i:
        test_wordpos.write(str(x[0]) + "_" + str(x[1]) + "\t" + str(x[2]) + "\n")
    test_wordpos.write("\n")

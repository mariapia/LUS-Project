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

lexicon_wordlemma = open("../lexicon_wordlemma.txt", "w")

train_wordlemma = open("../train_wordlemma", "w")
validation_wordlemma = open("../validation_wordlemma", "w")
test_wordlemma = open("../test_wordlemma", "w")

Seed = 463
random.seed(Seed)
split_f = train_feat.read().split('\n')
split_t = train_file.read().split('\n')

word_lemma = []
word_lemma_line = []
word_lemma_sentences = []

for x,y in zip(split_t, split_f):
    if x != '' and y != '':
        a, b = x.split('\t')  #word iob
        c, d, e = y.split('\t') #word pos lemma
        word_lemma.append((a, e))
        word_lemma_line.append((a, e, b))
    else:
        if len(word_lemma_line) != 0:
            word_lemma_sentences.append(word_lemma_line)
            word_lemma_line = []

split_feat = test_feat.read().split('\n')
split_test = test_file.read().split('\n')


test_data_wordlemma_sentences = []
test_data_wordlemma_line = []

for x,y in zip(split_test, split_feat):
    if x != '' and y != '':
        a, b = x.split('\t')  #word iob
        c, d, e = y.split('\t') #word pos lemma
        test_data_wordlemma_line.append((a, e, b))
    else:
        if len(test_data_wordlemma_line) != 0:
            test_data_wordlemma_sentences.append(test_data_wordlemma_line)
            test_data_wordlemma_line = []

##################################################################################################################
#                                          LEXICON WORD

counted_wordlemma = Counter(word_lemma)
count = 0

for i in counted_wordlemma:
    lexicon_wordlemma.write(str(i[0]) + "_" + str(i[1]) + "\t" + str(count) + "\n")
    count += 1
lexicon_wordlemma.write("<UNK>\t" + str(count) + "\n")

##################################################################################################################

length_sentences_wordlemma = len(word_lemma_sentences)
perc = length_sentences_wordlemma * float(sys.argv[1])
random.shuffle(word_lemma_sentences)

train_data_wordlemma = word_lemma_sentences[:int(perc)]
validation_data_wordlemma = word_lemma_sentences[int(perc):]

for i in train_data_wordlemma:
    for x in i:
        train_wordlemma.write(str(x[0]) + "_" + str(x[1]) + "\t" + str(x[2]) + "\n")
    train_wordlemma.write("\n")

for i in validation_data_wordlemma:
    for x in i:
        validation_wordlemma.write(str(x[0]) + "_" + str(x[1]) + "\t" + str(x[2]) + "\n")
    validation_wordlemma.write("\n")


for i in test_data_wordlemma_sentences:
    for x in i:
        test_wordlemma.write(str(x[0]) + "_" + str(x[1]) + "\t" + str(x[2]) + "\n")
    test_wordlemma.write("\n")

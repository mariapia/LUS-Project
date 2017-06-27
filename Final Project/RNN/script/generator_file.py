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

lexicon_word = open("../lexicon_word.txt", "w")
lexicon_label = open("../lexicon_label.txt", "w")

training_set = open("../training_set", "w")
validation_set = open("../validation_set", "w")

Seed = 463
random.seed(Seed)
split_f = train_feat.read().split('\n')
split_t = train_file.read().split('\n')

words = []
iob = []
line = []
sentences = []

for x,y in zip(split_t, split_f):
    if x != '' and y != '':
        a, b = x.split('\t')  #word iob
        c, d, e = y.split('\t') #word pos lemma
        words.append(a)
        iob.append(b)
        line.append((a, b))
    else:
        if len(line) != 0:
            sentences.append(line)
            line = []

split_feat = test_feat.read().split('\n')
split_test = test_file.read().split('\n')

for x,y in zip(split_test, split_feat):
    if x != '' and y != '':
        a, b = x.split('\t')  #word iob
        c, d, e = y.split('\t') #word pos lemma
        iob.append(b)



###########################################################################################################
#                   LEXICON WORD

counted_words = Counter(words)
conta = 0

for i in counted_words:
    lexicon_word.write(str(i) + "\t" + str(conta) + "\n")
    conta += 1

lexicon_word.write("<UNK>\t" + str(conta) + "\n")

###########################################################################################################
#                   LEXICON IOB

counted_iob = Counter(iob)
conta1 = 0

for i in counted_iob:
    lexicon_label.write(str(i) + "\t" + str(conta1) + "\n")
    conta1 += 1

###########################################################################################################

length_sentences = len(sentences)
perc_training = length_sentences * sys.argv[1]
random.shuffle(sentences)

train_data = sentences[:int(perc_training)]
validation_data = sentences[int(perc_training):]

for i in train_data:
    for x in i:
        training_set.write(str(x[0]) + "\t" + str(x[1]) + "\n")
    training_set.write("\n")

for i in validation_data:
    for x in i:
        validation_set.write(str(x[0]) + "\t" + str(x[1]) + "\n")
    validation_set.write("\n")



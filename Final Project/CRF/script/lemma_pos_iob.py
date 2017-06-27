#! /usr/bin/python3

"""
Language Understanding Systems Project
Student: Maria Pia Natale
ID number: 189160

"""
import sys
import math
from collections import Counter

train_file = open("../NLSPARQL.train.data", "r")
train_feat = open("../NLSPARQL.train.feats.txt", "r")
test_file = open("../NLSPARQL.test.data", "r")
test_feat = open("../NLSPARQL.test.feats.txt", "r")

word_lemma_pos_iob_train_file = open("../word_lemma_pos_iob_train.txt", "w")
word_lemma_pos_iob_test_file = open("../word_lemma_pos_iob_test.txt", "w")

word_lemma_pos_iob_train = []
word_lemma_pos_iob_test = []

split_f = train_feat.read().split('\n')
split_t = train_file.read().split('\n')

length = sys.argv[1]

for x,y in zip(split_t, split_f):
    if x != '' and y != '':
        a, b = x.split('\t')  #word iob
        c, d, e = y.split('\t') #word pos lemma
        if len(str(a)) >= int(length):
            prefix = a[0:int(length)]
            suffix = a[-int(length):]
        else:
            prefix = "NONE"
            suffix = "NONE"

        word_lemma_pos_iob_train.append((a, e, d, prefix, suffix, b))
    else:
        word_lemma_pos_iob_train.append("\n")


split_f = test_feat.read().split('\n')
split_t = test_file.read().split('\n')

for x,y in zip(split_t, split_f):
    if x != '' and y != '':
        a, b = x.split('\t')  #word iob
        c, d, e = y.split('\t') #word pos lemma
        if len(str(a)) >= int(length):
            prefix = a[0:int(length)]
            suffix = a[-int(length):]
        else:
            prefix = "NONE"
            suffix = "NONE"

        word_lemma_pos_iob_test.append((a, e, d, prefix, suffix, b))
    else:
        word_lemma_pos_iob_test.append("\n")


for x in word_lemma_pos_iob_train:
    if x != "\n":
        word_lemma_pos_iob_train_file.write(str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]) + "\t" + str(x[3]) + "\t" + str(x[4]) + "\t" + str(x[5]) + "\n")
    else:
        word_lemma_pos_iob_train_file.write(str(x))

for x in word_lemma_pos_iob_test:
    if x != "\n":
        word_lemma_pos_iob_test_file.write(str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]) + "\t" + str(x[3]) + "\t" + str(x[4]) + "\t" + str(x[5]) + "\n")
    else:
        word_lemma_pos_iob_test_file.write(str(x))

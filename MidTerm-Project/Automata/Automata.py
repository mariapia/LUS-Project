#! /usr/bin/python3
"""

Language Understanding Systems Project
Student: Maria Pia Natale
ID: 189160

This part of the LUS project creates two different transducers.

1st transducer LEMMA to IOB:
- each transition associates a lemma to an IOB concept tag
- the weight is computed by this formula

                        C( lemma, iob )
    p(lemma|iob) =  ------------------------
                            C(iob)


2nd transducer POS tag to IOB:
- each transition associates a POS tag to an IOB concept tag
- the weight is computed by this formula

                     C( pos, iob )
  p(pos|iob) =  ------------------------
                        C(iob)

:param: train_file = train file (NLSPARQL.train.data)
:param: train_feat = train file with features (NLSPARQL.train.feats.txt)
:param: test_file = test file (NLSPARQL.test.data)
:param: test_feat = test file with features (NLSPARQL.test.feats.txt)
:param: lemma_IOB_file = output file for the transducer from lemma to IOB concept tag
:param: pos_iob_file = output file for the transducer from POS tag to IOB concept tag
:param: lemma_notag_file = output file with all the lemma of the sentences without tags
:param: tagsentence_file = output file with all the tags for each sentence in the train file
:param: pos_notag_file = output file with all the POS tag of the sentences in the test file

"""
from collections import Counter
import sys
import math

train_file = open("NLSPARQL.train.data", "r")
train_feat = open("NLSPARQL.train.feats.txt", "r")
test_file = open("NLSPARQL.test.data", "r")
test_feat = open("NLSPARQL.test.feats.txt", "r")

lemma_IOB_file = open("LEMMA_IOB/lemma_IOB.txt", "w")
pos_iob_file = open("PosIOB/pos_iob.txt", "w")
lemma_notag_file = open("LEMMA_IOB/lemma_notag.txt", "w")
tagsentence_file = open("LEMMA_IOB/tagsentence.txt", "w")
tagsentence_file_POSIOB = open("PosIOB/tagsentence.txt", "w")
pos_notag_file = open("PosIOB/pos_notag.txt", "w")

word_lemma_pos_iob = []
lemma_IOB = []
pos_iob = []

tmp_f = train_feat.read().split('\n')
tmp_t = train_file.read().split('\n')

for x, y in zip(tmp_f, tmp_t):
    if x != '' and y != '':
        a, b, c = x.split('\t')
        d, e = y.split('\t')
        word_lemma_pos_iob.append((d, c, b, e))
        lemma_IOB.append((c, e))
        pos_iob.append((b, e))

train_file.close()

train_file = open("NLSPARQL.train.data", "r")
tmp_train = train_file.read().split('\n')
for line in tmp_train:
    if line != '':
        x, y = line.split('\t')
        tagsentence_file.write(y + " ")
        tagsentence_file_POSIOB.write(y + " ")
    else:
        tagsentence_file.write("\n")
        tagsentence_file_POSIOB.write("\n")
train_file.close()

tmp_test = test_feat.read().split('\n')
for line in tmp_test:
    if line != '':
        x, y, z = line.split('\t')
        lemma_notag_file.write(z + " ")
        pos_notag_file.write(y + " ")
    else:
        lemma_notag_file.write("\n")
        pos_notag_file.write("\n")

words = []
POStags = []
lemma = []
IOBtag = []
state = 0

for t in word_lemma_pos_iob:
    words.append(t[0])
    POStags.append(t[2])
    lemma.append(t[1])
    IOBtag.append(t[3])

words_uniq = list(set(words))
POStags_uniq = list(set(POStags))
lemma_uniq = list(set(lemma))
IOBtag_uniq = list(set(IOBtag))

###############################################################################################################
#                                                                                                             #
#                                                   LEXICON                                                   #
#                                                                                                             #
###############################################################################################################

lexicon_lemmaIOB_file = open("LEMMA_IOB/lexicon_lemmaIOB.txt", "w")
lexicon_POSIOB_file = open("PosIOB/lexicon_POSIOB.txt", "w")

count = 0
count2 = 0

lexicon_lemmaIOB_file.write("<eps>\t" + str(count) + "\n")

for x in lemma_uniq:
    count += 1
    lexicon_lemmaIOB_file.write(str(x) + "\t" + str(count) + "\n")

for x in IOBtag_uniq:
    count += 1
    lexicon_lemmaIOB_file.write(str(x) + "\t" + str(count) + "\n")

lexicon_lemmaIOB_file.write("<unk>\t" + str(count+1) + "\n")



lexicon_POSIOB_file.write("<eps>\t" + str(count2) + "\n")

for x in POStags_uniq:
    count2 += 1
    lexicon_POSIOB_file.write(str(x) + "\t" + str(count2) + "\n")

for x in IOBtag_uniq:
    count2 += 1
    lexicon_POSIOB_file.write(str(x) + "\t" + str(count2) + "\n")

lexicon_POSIOB_file.write("<unk>\t" + str(count2+1))

###############################################################################################################
#                                                                                                             #
#                                                AUTOMA LEMMA - IOB                                           #
#                                                                                                             #
###############################################################################################################


counted_IOB = Counter(IOBtag)
counted_lemmaIOB = Counter(lemma_IOB)

for i in counted_lemmaIOB:
    lemma_IOB_file.write(str(state) + "\t" + str(state) + "\t" + str(i[0]) + "\t" + str(i[1]) + "\t" + str(-math.log(counted_lemmaIOB[i]/counted_IOB[i[1]])) + "\n")

for i in counted_IOB:
    lemma_IOB_file.write(str(state) + "\t" + str(state) + "\t<unk>\t" + str(i) + "\t" + str(-math.log(1/len(IOBtag_uniq))) + "\n")
lemma_IOB_file.write(str(state) + "\n")

###############################################################################################################
#                                                                                                             #
#                                                AUTOMA POS - IOB                                             #
#                                                                                                             #
###############################################################################################################

counted_posiob = Counter(pos_iob)

for i in counted_posiob:
    if float(counted_posiob[i]/counted_IOB[i[1]]) != 1.0:
        pos_iob_file.write(str(state) + "\t" + str(state) + "\t" + str(i[0]) + "\t" + str(i[1]) + "\t" + str(-math.log(counted_posiob[i]/counted_IOB[i[1]])) + "\n")

for i in counted_IOB:
    pos_iob_file.write(str(state) + "\t" + str(state) + "\t<unk>\t" + str(i) + "\t" + str(-math.log(1/len(IOBtag_uniq))) + "\n")

pos_iob_file.write(str(state) + "\n")

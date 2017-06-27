#! /usr/bin/python3

"""
Language Understanding Systems Project
Student: Maria Pia Natale
ID number: 189160

This part of the LUS project creates a Weighted Final-State Transducer that performs sequence labeling.
Each transition in the transducer takes as input a pair composed by lemma with POS tag and associates
these pairs to an IOB concept tag.
The weight for the transition is computed by this formula:

                           C((lemma, pos), iob )
  p((lemma,pos)|iob) =  --------------------------
                                  c(iob)


:param train_file = train file (NLSPARQL.train.data)
:param train_feat = train file with features (NLSPARQL.train.feats.txt)
:param test_file = test file (NLSPARQL.test.data)
:param test_feat = test file with features (NLSPARQL.test.  feats.txt)
:param lemmapos_iob_file = output file for the transducer (lemma_POStag) to IOB concept tag
:param tagsentence_file = output file with only the tags for each sentence
:param lemmapos_notag_file = output file with all the sentences without tags

"""

from collections import Counter
import sys
import math

train_file = open("NLSPARQL.train.data", "r")
train_feat = open("NLSPARQL.train.feats.txt", "r")
test_file = open("NLSPARQL.test.data", "r")
test_feat = open("NLSPARQL.test.feats.txt", "r")

lemmapos_iob_file = open("lemmapos_iob.txt", "w")
tagsentence_file = open("tagsentence.txt", "w")
lemmapos_notag_file = open("lemmapos_notag.txt", "w")

word_lemma_pos_iob = []
lemma_pos = []
lemmapos_iob = []
iob = []
state = 0

tmp_f = train_feat.read().split('\n')
tmp_t = train_file.read().split('\n')

for x, y in zip(tmp_f, tmp_t):
    if x != '' and y != '':
        a, b, c = x.split('\t')
        d, e = y.split('\t')
        word_lemma_pos_iob.append((d, c, b, e))
        lemma_pos.append((c, b))
        lemmapos_iob.append((c, b, e))
        iob.append(e)

train_file.close()

train_file = open("NLSPARQL.train.data", "r")
tmp = train_file.read().split('\n')
for line in tmp:
    if line != '':
        x, y = line.split('\t')
        tagsentence_file.write(y + " ")
    else:
        tagsentence_file.write("\n")
train_file.close()

tmp = test_feat.read().split('\n')
for line in tmp:
    if line != '':
        x, y, z = line.split('\t')
        lemmapos_notag_file.write(z + "$" + y + " ")
    else:
        lemmapos_notag_file.write("\n")

###############################################################################################################
#                                                                                                             #
#                                                   LEXICON                                                   #
#                                                                                                             #
###############################################################################################################

lexicon = open("lexicon.txt", "w")

counted_lemmapos = Counter(lemma_pos)
counted_iob = Counter(iob)

count = 0

lexicon.write("<eps>\t" + str(count) + "\n")
for i in counted_lemmapos:
    count += 1
    lexicon.write(i[0] + "$" + i[1] + "\t" + str(count) + "\n")

for i in counted_iob:
    count += 1
    lexicon.write(i + "\t" + str(count) + "\n")

lexicon.write("<unk>\t" + str(count+1) + "\n")

###############################################################################################################
#                                                                                                             #
#                                       TRANSDUCER LEMMA-POS to IOB                                           #
#                                                                                                             #
###############################################################################################################

counted_lemmapos_iob = Counter(lemmapos_iob)

for i in counted_lemmapos_iob:
    lemmapos_iob_file.write(str(state) + "\t" + str(state) + "\t" + str(i[0]) + "$" + str(i[1]) + "\t" + str(i[2]) + "\t" + str(-math.log(counted_lemmapos_iob[i]/counted_iob[i[2]])) + "\n")

for i in counted_iob:
    lemmapos_iob_file.write(str(state) + "\t" + str(state) + "\t<unk>\t" + str(i) + "\t" + str(-math.log(1/len(counted_iob))) + "\n")

lemmapos_iob_file.write(str(state) + "\n")

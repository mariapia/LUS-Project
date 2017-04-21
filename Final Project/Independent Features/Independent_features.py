#! /usr/bin/python3
"""

Language Understanding Systems Project
Student: Maria Pia Natale
ID: 189160

This part of project creates three different transducers. These transducers will be composed to obtain a transducer that
associates a word to an IOB concept tag.

1ft transducer WORD to LEMMA:
- each transition associates a word to a lemma
- the cost is 0 if a given word is always transduced into a single lemma, otherwise the probability is given by the number
of times a given pair (word, lemma) appears divided by the total number of times that the word appears.

2nd transducer LEMMA to POS:
- each transition associates a lemma to the POS tag
- the probability is computed by using this formula:
                         C( lemma, POS )
    p(lemma|POS) =  ------------------------
                            C(POS)

3rd transducer POS to IOB:
- each transition associates a POS tag to an IOB concept tag
- the cost is computed by using this function:
                        C( POS, IOB )
    p(POS|IOB) =  ------------------------
                           C(IOB)


"""
from collections import Counter
import sys
import math


train_file = "NLSPARQL.train.data"
train_feat = "NLSPARQL.train.feats.txt"
test_file = "NLSPARQL.test.data"
test_feat = "NLSPARQL.test.feats.txt"
word_lemma_file = open("word_lemma.txt", "w")
lemma_pos_file = open("lemma_pos.txt", "w")
pos_iob_file = open("pos_iob.txt", "w")
tagsentence_file = open("tagsentence.txt", "w")
test_notag_file = open("test_notag.txt", "w")

file_data = []
IOBtag = []
with open(train_feat, "r") as f:
    tmp = f.read().split('\n')
    for line in tmp:
        if line != '':
            x, y, z = line.split('\t')
            file_data.append((x, y, z))

with open(train_file, "r") as f:
    tmp = f.read().split('\n')
    for line in tmp:
        if line != '':
            x, y = line.split('\t')
            IOBtag.append(y)
            tagsentence_file.write(y + " ")
        else:
            tagsentence_file.write("\n")

with open(test_file, "r") as f:
    tmp = f.read().split('\n')
    for line in tmp:
        if line != '':
            x, y = line.split('\t')
            test_notag_file.write(x + " ")
        else:
            test_notag_file.write("\n")
state = 0

#tuples (word_POStag_lemma) without duplicates
data_nodup = list(set(file_data))

#all words in TRAIN.FEAT
words = []

#all POStags in TRAIN.FEAT
POStags = []

#all lemmas in TRAIN.FEAT
lemma = []

for t in file_data:
    words.append(t[0])
    POStags.append(t[1])
    lemma.append(t[2])

words_uniq = list(set(words))
POStags_uniq = list(set(POStags))
lemma_uniq = list(set(lemma))
IOBtag_uniq = list(set(IOBtag))

###############################################################################################################
#                                                                                                             #
#                                                   LEXICON                                                   #
#                                                                                                             #
###############################################################################################################
lexicon_file = open("lexicon.txt", "w")
count = 0

lexicon_file.write("<eps>\t" + str(count) + "\n")
for i in words_uniq:
    count += 1
    lexicon_file.write(str(i) + "\t" + str(count) + "\n")

for i in POStags_uniq:
    count += 1
    lexicon_file.write(str(i) + "\t" + str(count) + "\n")

for i in lemma_uniq:
    if i not in words_uniq:
        count += 1
        lexicon_file.write(str(i) + "\t" + str(count) + "\n")

for i in IOBtag_uniq:
    count += 1
    lexicon_file.write(str(i) + "\t" + str(count) + "\n")

lexicon_file.write("<unk>\t" + str(count+1) + "\n")

###############################################################################################################
#                                                                                                             #
#                                             AUTOMA WORD - LEMMA                                             #
#                                                                                                             #
###############################################################################################################

#all couples word-lemma
word_lemma = []

for x in file_data:
    word_lemma.append((x[0], x[2]))

counted_wordlemma = Counter(word_lemma)
counted_words = Counter(words)
counted_POStags = Counter(POStags)
counted_lemma = Counter(lemma)
counted_IOB = Counter(IOBtag)

for x in counted_wordlemma:
    if (counted_wordlemma[x]/counted_words[x[0]]) != 1.0:
         word_lemma_file.write(str(state) + "\t" + str(state) + "\t" + str(x[0]) + "\t" + str(x[1]) + "\t" + str(-math.log(counted_wordlemma[x]/counted_words[x[0]])) + "\n")
    else:
         word_lemma_file.write(str(state) + "\t" + str(state) + "\t" + str(x[0]) + "\t" + str(x[1]) + "\t" + str(0) + "\n")

for l in lemma_uniq:
    if l not in words_uniq:
        word_lemma_file.write(str(state) + "\t" + str(state) + "\t" + str(l) + "\t" + str(l) + "\t" + str(0) + "\n")

word_lemma_file.write(str(state) + "\t" + str(state) + "\t<unk>\t<unk>\t0\n")
word_lemma_file.write(str(state))


###############################################################################################################
#                                                                                                             #
#                                            AUTOMA LEMMA - POStag                                            #
#                                                                                                             #
###############################################################################################################

lemma_POStag = []

for x in file_data:
    lemma_POStag.append((x[2], x[1]))

counted_lemmaPOS = Counter(lemma_POStag)

for x in counted_lemmaPOS:
    if (math.log(counted_lemmaPOS[x]/counted_POStags[x[1]])) != 0.0:
        lemma_pos_file.write(str(state) + "\t" + str(state) + "\t" + str(x[0]) + "\t" + str(x[1]) + "\t" + str(-math.log(counted_lemmaPOS[x]/counted_POStags[x[1]])) + "\n")
    else:
        lemma_pos_file.write(str(state) + "\t" + str(state) + "\t" + str(x[0]) + "\t" + str(x[1]) + "\t" + str(100) + "\n")

for i in counted_POStags:
        lemma_pos_file.write(str(state) + "\t" + str(state) + "\t<unk>\t" + str(i) + "\t" + str(-math.log(1/len(POStags_uniq))) + "\n")
lemma_pos_file.write(str(state) + "\n")

###############################################################################################################
#                                                                                                             #
#                                               AUTOMA POStag IOB                                             #
#                                                                                                             #
###############################################################################################################

POS_IOB = []

with open(train_feat, "r") as f, open(train_file, "r") as t:
    tmp_f = f.read().split('\n')
    tmp_t = t.read().split('\n')

    for x, y in zip(tmp_f, tmp_t):
        if x != '' and y != '':
            a, b, c = x.split('\t')
            d, e = y.split('\t')
            POS_IOB.append((b, e))


counted_POSIOB = Counter(POS_IOB)

for x in counted_POSIOB:
    if (math.log(counted_POSIOB[x]/counted_IOB[x[1]])) != 0.0:
        pos_iob_file.write(str(state) + "\t" + str(state) + "\t" + str(x[0]) + "\t" + str(x[1]) + "\t" + str(-math.log(counted_POSIOB[x]/counted_IOB[x[1]])) + "\n")
    else:
        pos_iob_file.write(str(state) + "\t" + str(state) + "\t" + str(x[0]) + "\t" + str(x[1]) + "\t" + str(100) + "\n")

for i in counted_IOB:
    pos_iob_file.write(str(state) + "\t" + str(state) + "\t<unk>\t" + str(i) + "\t" + str(-math.log(1/len(IOBtag_uniq))) + "\n")

pos_iob_file.write(str(state) + "\n")

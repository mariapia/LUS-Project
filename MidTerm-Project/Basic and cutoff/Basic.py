#! /usr/bin/python3
"""

Language Understanding Systems Project
Student: Maria Pia Natale
ID: 189160

This is the basic part of the LUS project.
The transducer that is created associates a word to an IOB concept tag. The weight of the transition
is computed by this formula:

                     C( word, iob )
    p(w|iob) =  ------------------------
                         C(iob)

:param input_file = train file (NLSPARQL.train.data)
:param output_file = output file for the transducer word to IOB concept tag
:param tagsentence_file = output file with all the tags for each sentence in the train file
:param test_notag_file = output file with all the words of the sentences without tags
:param test_file = test file (NLSPARQL.test.data)
:param lexicon = lexicon file

CUT-OFF

In this part words with frequency upper or lower than a bound are cut-off and the probabilities are computed
after the cut-off.

:arg upperbound = words with frequency upper than this bound are cut-off ( 0 if no cut-off is needed )
:arg lowerbound = words with frequency lower than this bound are cut-off ( 0 if no cut-off is needed )

"""
from collections import Counter
import sys
import math

input_file = "NLSPARQL.train.data"
output_file = open("basic.txt", "w")
tagsentence_file = open("tagsentence.txt", "w")
test_notag_file = open("test_notag.txt", "w")
test_file = "NLSPARQL.test.data"

lexicon = open("lexicon.txt", "w")

upperbound = sys.argv[1]
lowerbound = sys.argv[2]


file_data = []
test_data = []

with open(input_file, "r") as f:
    tmp = f.read().split('\n')
    for line in tmp:
        if line != '':
            x, y = line.split('\t')
            file_data.append((x, y))
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

words = []
tags = []

for t in file_data:
    tags.append(t[1])
    words.append(t[0])

num_tag = Counter(tags)
num_words = Counter(words)

single_tag = list(set(tags))
state = 0

###############################################################################################################
#                                                                                                             #
#                                                   LEXICON                                                   #
#                                                                                                             #
###############################################################################################################

count = 0
lexicon.write("<eps>\t" + str(count) + "\n")

for x in num_words:
    count += 1
    lexicon.write(str(x) + "\t" + str(count) + "\n")

for x in num_tag:
    count += 1
    lexicon.write(str(x) + "\t" + str(count) + "\n")

lexicon.write("<unk>\t" + str(count+1) + "\n")

###############################################################################################################
#                                                                                                             #
#                                           TRANSDUCER WORD to IOB                                            #
#                                                                                                             #
###############################################################################################################

occurences = Counter(file_data)
weight = []

for x in num_tag:
    for y in occurences:
        if x == y[1]:
            weight.append((y[0], y[1], -math.log(occurences[y]/num_tag[x]), occurences[y]))


weight.sort()

for x in weight:
    output_file.write(str(state) + "\t" + str(state) + "\t" + str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]) + "\n")
for i in single_tag:
    output_file.write(str(state) + "\t" + str(state) + "\t" + "<unk>" + "\t" + str(i) + "\t" + str(-(math.log(1/len(single_tag)))) + "\n")
output_file.write(str(state) + "\n")

###############################################################################################################
#                                                                                                             #
#                                             FREQUENCY CUT_OFF                                               #
#                                                                                                             #
###############################################################################################################

if int(upperbound) != 0 and int(lowerbound) != 0:
    file_frequencies_low = open("frequencies_low/frequencies_low.txt", "w")
    file_frequencies_up = open("frequencies_up/frequencies_up.txt", "w")
    couples_low = []
    couples_up = []
    tags_low = {}
    tags_up = {}
    lexicon_low_file = open("frequencies_low/lexicon_low.txt", "w")
    lexicon_up_file = open("frequencies_up/lexicon_up.txt", "w")
    lexicon_low = []
    lexicon_up = []
    count_low = 0
    count_up = 0

    for x in single_tag:
        tags_low[x] = 0
        tags_up[x] = 0

    for w in file_data:
        if num_words.get(w[0]) < int(lowerbound):
            tags_low[w[1]] = (int(tags_low[w[1]]) + 1)
        else:
            couples_low.append((w[0], w[1]))
            if lexicon_low.__contains__(w[0]) == False:
                lexicon_low.append(w[0])

    for w in file_data:
        if num_words.get(w[0]) > int(upperbound):
            tags_up[w[1]] = (int(tags_up[w[1]]) + 1)
        else:
            couples_up.append((w[0], w[1]))
            if lexicon_up.__contains__(w[0]) == False:
                lexicon_up.append(w[0])

    lexicon_low_file.write("<eps>\t" + str(count_low) + "\n")
    lexicon_up_file.write("<eps>\t" + str(count_up) + "\n")

    for x in lexicon_low:
        count_low += 1
        lexicon_low_file.write(str(x) + "\t" + str(count_low) + "\n")

    for x in lexicon_up:
        count_up += 1
        lexicon_up_file.write(str(x) + "\t" + str(count_up) + "\n")

    for x in single_tag:
        count_low += 1
        count_up += 1
        lexicon_low_file.write(str(x) + "\t" + str(count_low) + "\n")
        lexicon_up_file.write(str(x) + "\t" + str(count_up) + "\n")

    lexicon_low_file.write("<unk>\t" + str(count_low+1) + "\n")
    lexicon_up_file.write("<unk>\t" + str(count_up+1) + "\n")

    counted_low = Counter(couples_low)
    counted_up = Counter(couples_up)

    uniq_up = list(set(couples_up))
    uniq_low = list(set(couples_low))

    #TRANSDUCER FOR WORDS WITH FREQUENCY LESS THAN A LOWERBOUND

    for i in counted_low:
        prob = -math.log(float(counted_low[i]/(int(num_tag[i[1]]) - int(tags_low[i[1]]))))
        file_frequencies_low.write(str(state) + "\t" + str(state) + "\t" + str(i[0]) + "\t" + str(i[1]) +
                                   "\t" + str(prob) + "\n")


    for x in tags_low:
        if num_tag[x]-tags_low[x] != 0:
            file_frequencies_low.write(str(state) + "\t" + str(state) + "\t<unk>\t" + str(x) + "\t" +
                                       str(-math.log((num_tag[x]-tags_low[x])/(sum(val for key, val in num_tag.items()) - sum(val for key, val in tags_low.items())))) + "\n")

    file_frequencies_low.write("0")

    #TRANSDUCER FOR WORDS WITH FREQUENCY LESS THAN A UPPERBOUND

    for i in counted_up:
        prob = -math.log(float(counted_up[i]/(int(num_tag[i[1]]) - int(tags_up[i[1]]))))
        file_frequencies_up.write(str(state) + "\t" + str(state) + "\t" + str(i[0]) + "\t" + str(i[1]) +
                                   "\t" + str(prob) + "\n")

    for x in tags_up:
        if num_tag[x]-tags_up[x] != 0:
            file_frequencies_up.write(str(state) + "\t" + str(state) + "\t<unk>\t" + str(x) + "\t" +
                                       str(-math.log((num_tag[x]-tags_up[x])/(sum(val for key, val in num_tag.items()) - sum(val for key, val in tags_up.items())))) + "\n")

    file_frequencies_up.write(str(state) + "\n")





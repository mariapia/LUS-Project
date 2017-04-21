#! /bin/bash

################################################################################################################################
#INSTRUCTIONS:
#@param: order
#@param: smoothing method
#
################################################################################################################################

lexicon="lexicon.txt"
automa="basic.fst"
input="test_notag.txt"
output="automata_"$2"_"$1
evaluation="eval_"$2"_"$1

sentence_counter=0
mkdir $2

> $2/$output
farcompilestrings --symbols=$lexicon --unknown_symbol='<unk>' tagsentence.txt > tagsentence.far
while read -r line
do
	ngramcount --order=$1 --require_symbols=false tagsentence.far > pos$2$1.cnt
	ngrammake --method=$2 pos$2$1.cnt > pos$2$1.lm
	echo "$line" | farcompilestrings --symbols=$lexicon --unknown_symbol='<unk>' --generate_keys=1 --keep_symbols | farextract --filename_suffix='.fst'
	fstcompose 1.fst $automa | fstcompose - pos$2$1.lm | fstrmepsilon | fstshortestpath | fsttopsort | fstprint --isymbols=$lexicon --osymbols=$lexicon >> $2/$output
	echo " " >> $2/$output
	((sentence_counter++))
	echo "Line $sentence_counter: $line"
done < $input

awk '{print $4}' < $2/$output | awk -v RS= -v ORS="\n\n" "1" > tmp.txt
paste NLSPARQL.test.data tmp.txt > $2/final_$2_$1.txt

perl conlleval.pl -d "\t" < $2/final_$2_$1.txt > $2/$evaluation
rm tmp.txt pos* 1.fst tagsentence.far 

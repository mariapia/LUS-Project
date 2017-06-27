#! /bin/bash

./Basic.py $1 $2
fstcompile --isymbols=lexicon.txt --osymbols=lexicon.txt basic.txt > basic.fst
./elaborator.sh $3 $4

if [ $1 != 0 ] && [ $2 != 0 ]; then
    	fstcompile --isymbols=frequencies_low/lexicon_low.txt --osymbols=frequencies_low/lexicon_low.txt frequencies_low/frequencies_low.txt > frequencies_low/frequencies_low.fst
	fstcompile --isymbols=frequencies_up/lexicon_up.txt --osymbols=frequencies_up/lexicon_up.txt frequencies_up/frequencies_up.txt > frequencies_up/frequencies_up.fst

    cd frequencies_low
    ./elaborator.sh $3 $4
    cd ../frequencies_up    
    ./elaborator.sh $3 $4
fi

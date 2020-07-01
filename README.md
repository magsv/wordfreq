# wordfreq
A small python script to count frequencies of words including tokenization, stemming/lemming, removal of stop words++

Accepts path to a text file as an input and will then count frequencies in text using nltk and prior to that perform cleansing on words


## Requires that 

NLTK is installed


## Running

python3 -m categorizetext --inputfile=./hello.txt --resultfile=./results.csv --additional_stopwords=./addwords.txt 
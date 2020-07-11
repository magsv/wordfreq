import logging
import glob 
import os
import shutil
import click
import nltk
import csv
from os import path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

def remove_uoms(words):
    """
    Remove uoms in the form of e.g. 1000m 1543m3

    Parameters
    ----------
    words: list of words to process

    Returns
    -------

    A list of words where possible uom have been removed
    """

    returnWords=[]
    for word in words:
        word=word.replace('.', '', 1)
        word=word.replace(',', '', 1)
        if word[0:len(word)-1].isnumeric()==False and word[0:len(word)-1].isdecimal()==False:
            #we do not have a match on e.g. 1543m 
            if word[0:len(word)-2].isnumeric()==False and word[0:len(word)-2].isdecimal()==False:
                #we do not have a match on e.g. 1543m3
                #add it
                returnWords.append(word)
    return returnWords

        

def remove_single_char_tokens(words):
    """
    Removes single char tokens e.g punctum

    Parameters
    -----------
    words: list of words to process

    Returns
    -------
    Processed list of words where single char tokens has been removed
    """
    return [word for word in words if len(word) > 1]

def remove_numerics(words):
    """
    Removes numerics

    Parameters
    -----------
    words: list of words to process

    Returns
    -------
    Processed list of words where numbers have been removed
    """
    return [word for word in words if not word.isnumeric()]

def remove_decimals(words):
    """
    Removes decimals

    Parameters
    -----------
    words: list of words to process

    Returns
    -------
    Processed list of words where decimals have been removed
    """
    return [word for word in words if not '.' in word and not ',' in word]

def lowercase_words(words):
    """
    Lowercases a list of words

    Parameters
    -----------
    words: list of words to process

    Returns
    -------
    Processed list of words where words are now all lowercase
    """
    return [word.lower() for word in words]


def stem_words(words):
    """
    Runs Porter Stemming from NLTK on list of words

    Parameters
    -----------
    words: list of words to process

    Returns
    -------
    Processed list of words where each word is now stemmed
    """
    ps =PorterStemmer()
    wordReturn=[]
    for word in words:
        wordReturn.append(ps.stem(word))
    return wordReturn

def lemmentize_words(words):
    """
    Runs WordNet lemmatizer from NLTK on list of words

    Parameters
    -----------
    words: list of words to process

    Returns
    -------
    Processed list of words where each word is now lemmatrized
    """
    result=[]
    lemmtizer = WordNetLemmatizer()
    for word in words:
        lem_word=lemmtizer.lemmatize(word)
        result.append(lem_word)
    return result

def count_frequency(words):
    """
    Runs frequency count on list of words using NLTK

    Parameters
    -----------
    words: list of words to process

    Returns
    -------
    List of frequencies in the form of [(word,frequence)] e.g. [('hello',132)]
    """
    fdist = nltk.FreqDist(words)
    return fdist

def write_frequency(csvfile,fdist):
    """
    Writes frequency distribution to a csvfile

    Parameters
    -----------
    csvfile: csvfile to write
    fdist: frequence distribution

    """
    with open(csvfile, mode='w',newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Word","Frequency"])
        
        for word,frequency in fdist.items():
            writer.writerow([word,frequency])

def tokenize_and_remove_stopwords(txt,additional_stopwords):
    """
    Runs tokenization and removes stop words on the specified text

    Parameters
    -----------
    txt: text to process
    additional_stopwords: path to file containing possible additional stopwords on each line

    Returns
    -------
    Processed list of words where each word is now stemmed
    """
    logging.info("Removing stopwords")
    words_filter=load_stopwords(additional_stopwords)
    tokens=word_tokenize(txt)
    #make everything lowercase
    tokens=lowercase_words(tokens)
    tokens_without_sw=[]
    tokens_without_sw = [word for word in tokens if word not in words_filter]
    return tokens_without_sw

def load_stopwords(inputfile):
    """
    Loads additional stopwords to use from a file where each additional stopword is on a new line

    Parameters
    -----------
    inputfile: path to file containing stop words

    Returns
    -------
    List of stopwords including default english ones from nltk and additional from specified file
    """
    additional_words=[]
    if inputfile!=None:
        additional_words=read_lines_from_file(inputfile)
    stop_words=stopwords.words('english')
    for item in additional_words:
        logging.info("Adding additional stopword:%s",item)
        stop_words.append(str(item))
        stop_words.append(str(item).upper())
    return stop_words

def classify_text(inputfile):
    """
    Reads text from a file
    """
    txt=read_text_from_file(inputfile)
    return txt

def read_text_from_file(inputfile):
    f = open(inputfile, "r")
    return f.read()
    
def read_lines_from_file(inputfile):
    lines=[]
    with open(inputfile, 'r') as fh:
        for line in fh:
            line = line.rstrip("\n")
            lines.append(line)
    return lines


def categorizetext(inputfile,resultfile,additional_stopwords,
lemmetize=True,stem=True,numerics=True,uoms=True,singlechars=True,
decimals=False):
    txt=read_text_from_file(inputfile)
    words=tokenize_and_remove_stopwords(txt,additional_stopwords)
    if singlechars:
        logging.info('Running removale of single chars')
        words=remove_single_char_tokens(words)
    if decimals:
        logging.info('Running removal of decimals')
        words=remove_decimals(words)
    if numerics:
        logging.info('Running removal of numerics')
        words=remove_numerics(words)
    if uoms:
        logging.info('Running removal of uoms')
        words=remove_uoms(words)
    if lemmetize:
        logging.info('Running lemmitization')
        words=lemmentize_words(words)
    if stem:
        logging.info('Running stemming')
        words=stem_words(words)
    freq=count_frequency(words)
    write_frequency(resultfile,freq)
    print ("Wrote file to:"+resultfile)
    logging.info("Wrote file to:%s",resultfile)


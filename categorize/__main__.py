import logging
import glob 
import os
import shutil
import click
import os.path
import nltk
import csv
from os import path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import categorize.freq_utils as futils
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

@click.group()
def messages():
  pass

def create_filepath_if_not_exists(filepath):
    """
    Creates the given filepath path if not existing
    """
    dirname=os.path.dirname(filepath)
    #check if it exists or not
    if os.path.exists(dirname)==False:
        os.makedirs(dirname)

def initialize_logging(logfile):
    create_filepath_if_not_exists(logfile)
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
    logging.FileHandler(logfile),
    logging.StreamHandler()
    ]
    )

def create_folderpath_if_not_exists(dirname):
    """
    Creates the given filepath path if not existing
    """
    #check if it exists or not
    if os.path.exists(dirname)==False:
        os.makedirs(dirname)

@click.command(name='categorizetext',help='Command to extract information from text to a output file')
@click.option('--inputfile',
              help='The inputfile containing the text to analyze',
              required=True)
@click.option('--resultfile',
              help='The full path to file where to store analyzed text',
              required=True)
@click.option('--additional_stopwords',
              help='The path to a file containing additional stopwords to use in addition to english stopwords from nltk. Each stopword separated by newline',
              required=False)   
@click.option('--logfile',
              help='The full path logfile to use',
              required=True)
@click.option('--lemmetize', is_flag=True,default=False,help='If specifified runs lemmetization on words')
@click.option('--stem', is_flag=True,default=False,help='If specified runs stemming on words')
@click.option('--numerics', is_flag=True,default=False,help='If specified tries to remove numerics')
@click.option('--uoms', is_flag=True,default=False,help='If specified tries to remove uom e.g. m3')
@click.option('--singlechars', is_flag=True,default=False,help='If specified removes singlechars')
@click.option('--decimals', is_flag=True,default=False,help='If specified removes decimals')
def categorizetext(inputfile,resultfile,additional_stopwords,logfile,
lemmetize,stem,numerics,uoms,singlechars,decimals):
    initialize_logging(logfile)
    futils.categorizetext(inputfile,resultfile,additional_stopwords,
    lemmetize,stem,numerics,uoms,singlechars,decimals)




@click.command()
@click.pass_context
def help(ctx):
    print(ctx.parent.get_help())



messages.add_command(categorizetext)
messages.add_command(help)


if __name__ == '__main__':
    messages()


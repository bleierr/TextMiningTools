'''
Created on 19 Jan 2015

@author: Rombli
'''
from txt_classes import TxtCorpus
from cleaner import remove_stopwords, stem_txt
from settings import CORPUS_PATH
from import_excel import get_data_from_Excel
import os

def run_func_on_corpus(func, *args, **kwargs):
    """
    runs a function on the corpus file
    @func: the function that will be run on the corpus of txt files, the first argument of func, a string, is
    passed in from each corpus file.
    """
    c = TxtCorpus(CORPUS_PATH)
    strg = ''
    new_strg = ''
    for txt in c.get_txtitems():
        with open(txt.get_file_path(), "r") as f:
            strg = f.read()
        new_strg = func(strg, *args, **kwargs)
        with open(txt.get_file_path(), "w") as f:
            f.write(new_strg)
    return True


if __name__ == '__main__':
    
    s = "ll dr hon le je il dont en lbs les yr mon carson didn oct sec je brien sd arm des".split()
    
    test_data = 'C:' + os.sep +'TestTexts' + os.sep + 'TestData' + os.sep + 'all_transcriptions_until_16_06_2014.xlsx'
    txts = get_data_from_Excel(test_data)
    
    
    #run_func_on_corpus(remove_stopwords, s)
    
    run_func_on_corpus(stem_txt)
    
    print "Done!"
    
    
    
    
    
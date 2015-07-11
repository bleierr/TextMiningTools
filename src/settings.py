import os
from nltk import corpus

#DEFAULT FILE PATH Importer
IMP_KEY_ARGS = {}

IMP_KEY_ARGS["file_name_excel"] = "C:" + os.sep + "TestTexts" + os.sep + "TestData" + os.sep + "1916letters_all_translations12012015.xlsx"

IMP_KEY_ARGS["corpus_dir"] = "C:" + os.sep + "TestTexts" + os.sep + "1916letters_all_translations12012015"
    
IMP_KEY_ARGS["txt_dir_path"] = "C:" + os.sep + "TestTexts" + os.sep + "1916letters_all_translations12012015" + os.sep + "txt"

IMP_KEY_ARGS["mode"] = "excel"


#Corpus path to TxtCorpus
CORPUS_PATH = "C:" + os.sep + "TestTexts" + os.sep + "1916letters_all_translations12012015" + os.sep + "corpusfiles.pickle"


STOPWORD_LST = corpus.stopwords.words("english") + ["&", "&amp;"] 
STOPWORD_FILE = "letters_stopwords.txt" #if not stopword file is used 'None' has to be added

SPELL_CHECK_PWL = "letters_pwl.txt" #if no personal word list is used the variable has to be set to 'None'


#standard cleaning pattern
CLEANING_PATTERN = [("no-group", "<unclear>questionable reading</unclear>"), # appeared in letter 1004 several times
                    ("no-group", "<[/\w\d\s\"\'=]+>|<!--[/\w\d\s\"\'=\.,-]+-->"),
                    ("no-group", "[\d\.]+[ap]m"), #remove times e.g. 5pm or 4.30pm
                    ("no-group", "\'s"), #remove Gen. 's' e.g. Paul's
                    ("no-group", "[\d/'\.]+"),
                    ("no-group", "\s(\w\.)+\s"),
                    ("no-group", "&[#\w\d]+;"), 
                    ("use-group", "[\W]*(\w+[\w\'-/\.]*\w+|\w|&)[\W]*")
                     ] # 1916 letter cleaning pattern
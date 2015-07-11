'''
Created on 13 May 2014

This module contains the letter class
@author: Bleier
'''
from settings import CLEANING_PATTERN, STOPWORD_LST, STOPWORD_FILE, SPELL_CHECK_PWL, IMP_KEY_ARGS
from helper import item_to_shelve, get_text_files
from nltk import stem
import enchant
import re, os, shutil, getopt, sys
import txt_classes, settings

def remove_hapax_lego(texts):
    """
    texts is a list of lists: corpus = [["this", "is", "a", "crazy", "idea"], ["all", "ideas", "are", "crazy"], ["this", "a"]]     
    return will be a list of lists: [['this', 'a', 'crazy'], ['crazy'], ['this', 'a']]
    """
    all_tokens = sum(texts, [])
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once]
         for text in texts]
    return texts

def clean_with_pattern(strg):
    """
    cleans a text according to a pattern defined in settings.py
    The CLEANING_PATTERN is a list of tuples the first element of the tuple contains 'no-group' or 'use-group, the second a regex pattern to be used
    'no-group' means the text will be cleaned of occurrences of pattern, while 'use-group' will keep the pattern defined in the group  
    Possible uses: Strips xml markup from string, splits a string into word token, strips leading and trailing punctuation and white space
    Parameter strg is a string, the function returns a list of strings
    Returns the text as a list words cleaned of the defined pattern(s)
    """
    for type, pat in CLEANING_PATTERN:
        if type == "no-group":
            strg = " ".join(re.split(pat , strg))
        elif type == "use-group":
            regex = re.compile(pat)
            lst = []
            for item in strg.split():
                mm = regex.match(item)
                if mm:
                    lst.append(mm.group(1))
            strg = " ".join(lst)
    return strg

def remove_stopwords(strg, stop_word_lst):
    words = strg.split()
    return " ".join([w for w in words if w not in stop_word_lst])








def spell_checking(wordlst):
    
    temp_pwl_file = "Temporary_pwl_file.txt"
    with open(SPELL_CHECK_PWL, "r") as f:
        all_pwl = f.read().lower()
        
    with open(temp_pwl_file, "w") as f:
        f.write(all_pwl)
        
    
    d = enchant.DictWithPWL("en_US", temp_pwl_file)
    err = []
    for w in wordlst:
        if not d.check(w):
            try:
                first_sug = d.suggest(w)[0]
                if w != first_sug.lower():
                    err.append((w, first_sug))
            except IndexError:
                err.append((w, None))
    os.remove(temp_pwl_file)
    return err

def stemmer(wordlst):
    st = stem.PorterStemmer()
    stem_words = []
    for w in wordlst:
        stem_words.append((w, st.stem(w)))
    return stem_words

def stem_txt(strg):
    words = strg.split()
    stem_words = stemmer(words)
    words = []
    for word, stemw in stem_words:
        words.append(stemw)
    return " ".join(words)
    
    
    
    

def clean_all(file_dir_path, clean_files_dir, mode="pat+stop"):
    #make a directory for the cleaning log
    stat_dir = clean_files_dir + os.sep + "cleaninglog"
    os.mkdir(stat_dir)
    
    filenames = get_text_files(file_dir_path, ext=".txt")
    
    spell_err = ""
    stem_print = ""
    for filename in filenames:
        file_path = file_dir_path + os.sep + filename
        with open(file_path, "r") as f:
            strg = f.read()
        if mode == "pat+stop":
            wordlst = clean_with_pattern(strg)
            wordlst = remove_stopwords(wordlst)
        else:
            wordlst = strg.split()
        item_to_shelve(stat_dir+os.sep+"wordlst.shelve", wordlst, filename)
        #check for spelling errors
        err_lst = spell_checking(wordlst)
        if mode == "spell":
            words = " ".join(wordlst)
            for err, corr in err_lst:
                if corr:
                    words = words.split(" "+err+" ")
                    words = " "+corr+" ".join(words)
            wordlst = words.split()
        if err_lst:
            spell_err += "\n{0}:\n".format(filename)
        
            for err, corr in err_lst:
                spell_err += "{0}:{1}\n".format(err, corr)
            
        #check for stemming
        stem_words = stemmer(wordlst)
        if mode == "stem":
            words = []
            for word, stemw in stem_words:
                words.append(stemw)
            wordlst = words
        
        stem_print += "\n{0}:\n".format(filename)
        for word, stemw in stem_words:
            stem_print += "{0}:{1}\n".format(word, stemw)
        
        with open(clean_files_dir + os.sep + filename, "w") as f:
            f.write(" ".join(wordlst))
        
    with open(stat_dir+os.sep+"spelling_errors.log", "w") as f:
        f.write(spell_err)
        
    with open(stat_dir+os.sep+"stem_froms.log", "w") as f:
        f.write(stem_print)
    
        
def cleaner_main(files_dir=None, clean_files_dir=None, mode="pat+stop"):
    if not files_dir:
        print files_dir
        print "No file path given for text files."
        return False
    if not clean_files_dir:
        clean_files_dir = os.path.split(os.path.abspath(files_dir))[0] + os.sep + "cleantxt"
        #make file dir for the clean txt files
    if os.path.isdir(clean_files_dir):
        inp = raw_input("The directory {0} does already exist. Overwrite?Y/N".format(clean_files_dir))
        if inp in ["Y", "y"]:
            shutil.rmtree(clean_files_dir)
        else:
            return False
    os.mkdir(clean_files_dir)
    
    clean_all(files_dir, clean_files_dir, mode=mode)
     
if __name__ == "__main__":
    """opts, args = getopt.getopt(sys.argv[1:], "", ["mode=", "files_dir=", "clean_files_dir="])
    key_args = {}
    for key, value in opts:
        if key == "--mode": # mode values: "pat+stop" (default), 'spell', 'stem'
            key_args["mode"] = value
        if key == "--files_dir":
            key_args["files_dir"] = value
        elif key == "--clean_files_dir":
            key_args["clean_files_dir"] = value
    cleaner_main(**key_args)"""
    
    files_dir = IMP_KEY_ARGS["txt_dir_path"]
    clean_files_dir = IMP_KEY_ARGS["corpus_dir"] + os.sep + "clean_txt"
    rem_hapax_dir = IMP_KEY_ARGS["corpus_dir"] + os.sep + "no_hapax_txt"
    #cleaner_main(files_dir, clean_files_dir, mode="pat+stop")
    """
    files = os.listdir(files_dir)
    for fil in files:
        with open(files_dir +os.sep+ fil, "r") as f:
            no_pat = clean_with_pattern(f.read())
            cleaned = remove_stopwords(no_pat.split())
        with open(clean_files_dir+os.sep+fil, "w") as f:
            f.write(" ".join(cleaned))
    """
    
    corpus = txt_classes.TxtCorpus(settings.IMP_KEY_ARGS["corpus_dir"]+os.sep+"corpusfiles.pickle")
    #remove hapax legomena   
    """ 
    files = os.listdir(clean_files_dir)
    
    hapaxes = [text for text in corpus]
    
    print "done hapaxes"
    
    no_hap = remove_hapax_lego(hapaxes)
    
    print "done remove hapax"
    
    for i, o in enumerate(corpus.get_txtitems()):
        with open(rem_hapax_dir+os.sep+o.unique_name + ".txt", "w") as f:
            f.write(" ".join(no_hap[i]))
    """
    """
    num_words = 0
    files = os.listdir(rem_hapax_dir)
    for fil in files:
        with open(rem_hapax_dir + os.sep+ fil, "r") as f:
            words = f.read().split()
            num_words += len(words)
        with open(rem_hapax_dir + os.sep+fil, "w") as f:
            f.write(" ".join([w.lower() for w in words]))
    
    print num_words # words without hapax 113866
    
    
    #print remove_hapax_lego(corpus)
    """
    nodes = 'Id,Label,gender,topic,pages\n'
    for txt in corpus.get_txtitems():
        pages = len(txt.get_pages())
        if txt.Authors_gender is "Female;Female":
            gender = "female"
        else:
            gender = txt.Authors_gender.lower()
        nodes += "{0},{1},{2},{3},{4}\n".format(txt.Letter, txt.Letter, gender, txt.Collection, pages)
    
    with open(IMP_KEY_ARGS["corpus_dir"]+os.sep+"nodes.csv", "w") as f:
        f.write(nodes)
    
    print "done"
    
               
    
    
            
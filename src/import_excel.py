# coding=<utf-8>
'''
Created on 8 Jan 2015

@author: Rombli
'''
import xlrd, os, sys
import datetime
import re
import helper
import ner_nltk

TIMESTAMP_COL = "Translation_Timestamp" #"Translation_Timestamp"
PAGE_COL = "Page"
TRANSCRIPTION_COL = "Translation"
TXT_ID = "Letter"


class Bunch(object):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                raise AttributeError("API conflict: '%s' is part of the '%s' API" % (key, self.__class__.__name__))
            else:
                setattr(self, key, value)
                
    def get(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise AttributeError("No attribute '%s' found" % key)
        
class TxtCorpus(object):     
    def __init__(self, folder_path, data_file=None):
        self.corpus = folder_path
        self.data_file = data_file
        
    def __iter__(self):
        files = os.listdir(self.corpus)
        for file_item in files:
            file_path = self.corpus + os.sep + file_item
            with open(file_path, 'r') as f:
                yield f.read()
    
    def each(self, fun):
        files = os.listdir(self.corpus)
        for file_item in files:
            file_path = self.corpus + os.sep + file_item
            with open(file_path, 'r') as f:
                txt = f.read()
            with open(file_path, 'w') as f:
                f.write(fun(txt))


def get_data_from_Excel(file_name_excel):
    """
    The function gets data from an Excel file and turn it into a Bunch obj
    The parameter file_name_excel is a valid file path to an excel file containing texts and metadata
    A list with Bunch obj is returned
    """
    #Creates an object of type Book from xlrd.book object
    try:
        wb = xlrd.open_workbook(filename=file_name_excel, encoding_override="utf-8")
    except xlrd.XLRDError:
        print "The file at the location {} is not a valid excel format".format(file_name_excel)
        sys.exit()
    sheet = wb.sheet_by_index(0)
    texts = []
    try:
        for row in range(1,sheet.nrows):
            row_dict = {}
            for col in range(sheet.ncols):
                if sheet.cell(row,col).ctype == 3: # 1 is type text, 3 xldate
                    date_tuple = xlrd.xldate_as_tuple(sheet.cell_value(row,col), wb.datemode)
                    date_py = datetime.datetime(*date_tuple)
                    row_dict.update({sheet.cell_value(0,col): date_py}) # a datetime.datetime obj is stored
                else:
                    row_dict.update({sheet.cell_value(0,col):sheet.cell_value(row,col)})
            t = Bunch(**row_dict)
            texts.append(t)
        return texts
    except KeyError:
        print "KeyError: possible cause - column names in settings file are not found in the excel source file"
        sys.exit()
    
def find_latest_entries(lst):
    """The function is used to find the latest entries in a list of Bunch objects"""
    latest = {}
    for b in lst:
        entry_ID = b.get(TXT_ID)
        if entry_ID in latest:
            date1 = latest[entry_ID].get(TIMESTAMP_COL)
            date2 = b.get(TIMESTAMP_COL)
            if date1 < date2:
                latest[entry_ID] = b
        else:
            latest[entry_ID] = b
    return latest.values()

def dict_to_file(d, file_path):
    """Takes a dictionary (d) as argument and writes d to a csv file.
    The csv file has two columns 'key' 'value'.
    @d: a dictionary
    @file_path: is the file path under which the d will be saved
    """
    if (os.path.isfile(file_path)):
        raise OSError("File does already exist %s" % file_path) 
    with open(file_path, 'w') as f:
        for key, value in d.items():
            if type(value) is datetime.datetime:
                value = value.strftime("%Y%m%dT%H%M%S")
            if type(value) is float:
                value = str(value)
            v = helper.replace_problem_char(value.encode("utf-8"))
            f.write("{0}, {1}\n".format(key, v))
    
    
def list_to_folder(lst, folder_path):
    if not (os.path.isdir(folder_path)):
        os.mkdir(folder_path)
        print "Folder created: %s" % folder_path
    for b in lst:
        #b is a Bunch obj
        #d = b.__dict__
        file_name = "%s.txt" % b.get(TXT_ID)
        file_path = folder_path + os.sep + file_name
        with open(file_path, "w") as f:
            trans = helper.replace_problem_char(b.get(TRANSCRIPTION_COL).encode("utf-8"))
            f.write(trans)
 
def replaceA(strg):
    expr = re.compile("a")
    return expr.sub("", strg)

if __name__ == "__main__":
    data_dir = 'C:'+os.sep+'TestTexts'
    pickle_name = data_dir + os.sep + "stopword.pickle"
    """
    if os.path.isfile(file_path):
        l = get_data_from_Excel(file_path)  
        latest = find_latest_entries(l)
        list_to_folder(latest, corpus_path)
        
        c = TxtCorpus(corpus_path)
        print "Corpus created"
        #c.each(replaceA)
        count = 0
        
        
        
        helper.item_to_pickle(pickle_name, set())
        for txt in c:  
            count += 1  
            if count%100==0:
                print count
            stopw_set = helper.item_from_pickle(pickle_name) 
            helper.item_to_pickle(pickle_name, stopw_set | ner_nltk.build_ner_stopwordlst(txt))
            
        print "Finished creating stopword pickle"
        with open(data_dir + os.sep + "stopwordlist.txt", "w") as f:
            stopw_set = helper.item_from_pickle(pickle_name) 
            f.write("\n".join(stopw_set))
            
                        
        print len(l)
        print len(latest)
        
    else:
        print 'Filepath not correct: ' + file_path
    """
    
    stopw_set = helper.item_from_pickle(pickle_name)
    
    with open(data_dir + os.sep + "letters_stopwords.txt", "w+") as f: 
            f.write(" ".join(stopw_set))
    
    print("Done!")
    
    
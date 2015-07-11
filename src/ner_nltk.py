# coding=<utf-8>
'''
Created on 8 Jan 2015

@author: Rombli
'''

from nltk.tag.stanford import NERTagger
import os, settings, helper, txt_classes
import cleaner

#4 class model trained for CoNLL: Location, Person, Organization, Misc
model4classes = os.sep.join(['C:', 'TestTexts', 
                      'StanfordNER', 
                      'english.muc.4class.nodistsim.crf.ser.gz'])

#a 7 class model trained for MUC: Time, Location, Organization, Person, Money, Percent, Date
model7classes = os.sep.join(['C:', 'TestTexts', 
                      'StanfordNER', 
                      'english.muc.7class.nodistsim.crf.ser.gz'])

#3 class model trained on both data sets for the intersection of those class sets: Person, Location, Organisation
model3classes = os.sep.join(['C:', 'TestTexts', 
                      'StanfordNER', 
                      'english.all.3class.nodistsim.crf.ser.gz'])

jarfile = os.sep.join(['C:',
    'Users',
    'Rombli',
    'Downloads',
    'stanford-ner-2014-10-26',
    'stanford-ner-2014-10-26',
    'stanford-ner.jar'])

def run3ClassModel(strg):
    if not os.path.exists(model3classes):
        raise OSError("Failed to loading gz file: %s" % model3classes)

    if not os.path.exists(jarfile):
        raise OSError("Failed to loading jar file: %s" % jarfile)
    
    st = NERTagger(model3classes, jarfile)
    #returns a list of [('schoolmaster', 'O'), ('Irish', 'LOCATION'), ('Patrick', 'PERSON'), ('Pearse', 'PERSON'), ('.', 'O')...]  
    return st.tag(strg.split())

def run7ClassModel(strg):
    if not os.path.exists(model7classes):
        raise OSError("Failed to loading gz file: %s" % model7classes)

    if not os.path.exists(jarfile):
        raise OSError("Failed to loading jar file: %s" % jarfile)
    
    st = NERTagger(model7classes, jarfile)
    #returns a list of [('Monday', 'DATE'), ('schoolmaster', 'O'), ('Irish', 'LOCATION'), ('Patrick', 'PERSON'), ('Pearse', 'PERSON'), ('.', 'O')...]  
    return st.tag(strg.split())


def strip_words(func, strg, tags=None):
    """
    returns the string (strg) cleaned of found enties
    @func: the function to he executed to find the named entities, e.g.run7ClassModel(strg)
    @strg: a string of words
    @tags: a list of possible search tags identifying the entities that 
            should be stripped out, Default values are: ['PERSON', 'LOCATION', 'ORGANIZATION']
    return string, cleaned of the entities defined by @tags
    """
    w_lst = []
    
    if not tags:
        tags = ['PERSON', 'LOCATION', 'ORGANIZATION']
    
    for w, tag in func(strg):
        if tag not in tags:
            w_lst.append(w)
    
    return ' '. join(w_lst)

def get_named_entities(func, strg, tags=None):
    """
    returns a list of Named Entities found in the provided string (strg)
    @func: the function to he executed to find the named entities
    @strg: a string of words
    @tags: a list of possible search tags identifying the entities to 
            include into the returned list, Default values are: ['PERSON', 'LOCATION', 'ORGANIZATION']
    return value is a list of found entities, what values are found is specified by @tags
    """
    found_entities = {}
    
    if not tags:
        tags = ['PERSON', 'LOCATION', 'ORGANIZATION']
    
    for w, tag in func(strg):
        if tag in tags:
            if w not in found_entities:
                found_entities[w] = tag
    return found_entities
    
def build_ner_stopwordlst(strg):
    d3class = get_named_entities(run3ClassModel, strg)
    d7class = get_named_entities(run7ClassModel, strg, ['PERSON', 'LOCATION', 'ORGANIZATION', 'TIME', 'DATE'])
    return set(d3class) | set(d7class)

if __name__ == '__main__':
    test_txt = u"""Members of the Irish Volunteers led by schoolmaster and Irish language activist 
    Patrick Pearse, joined by the smaller Irish Citizen Army of James Connolly, 
    along with 200 members of Cumann na mBan seized Easter Monday, 24 April 1916, and lasted for six days
    key locations in Dublin and proclaimed the Irish Republic independent of the United Kingdom.""".encode("utf-8")
    
    #print build_ner_stopwordlst(test_txt)
    
    c = txt_classes.TxtCorpus(settings.IMP_KEY_ARGS["corpus_dir"]+os.sep+"corpusfiles.pickle")
    
    
    data_dir = settings.IMP_KEY_ARGS["corpus_dir"]
    count = 0
    pickle_name = data_dir + os.sep + "stopword.pickle"
        
    helper.item_to_pickle(pickle_name, set())
    for item in c:  
        txt = cleaner.clean_with_pattern(" ".join(item))
        count += 1  
        if count%100==0:
            print count
        stopw_set = helper.item_from_pickle(pickle_name) 
        helper.item_to_pickle(pickle_name, stopw_set | build_ner_stopwordlst(txt))
            
    print "Finished creating stopword pickle"
    with open(data_dir + os.sep + "stopwordlist.txt", "w") as f:
        stopw_set = helper.item_from_pickle(pickle_name) 
        f.write("\n".join(stopw_set))
    
    
    
    
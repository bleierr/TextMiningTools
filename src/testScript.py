'''
Created on 9 Jan 2015

@author: Rombli
'''
import os
import helper


if __name__ == '__main__':
    
    data_dir = 'C:'+os.sep+'TestTexts'
    pickle_name = data_dir + os.sep + "stopword.pickle"
    
    with open(data_dir + os.sep + "stopwordlist.txt", "w") as f:
            stopw_set = helper.item_from_pickle(pickle_name) 
            f.write("\n".join(stopw_set))
            
            
            
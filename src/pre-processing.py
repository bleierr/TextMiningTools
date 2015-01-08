'''
Created on 8 Jan 2015

@author: Rombli
'''


from nltk.tag.stanford import NERTagger

txt = "bureau de secours aux prissoniers de la guerrre section anglaise berne 5th january, 1916 sir, i am to-day in receipt of bread forwarded by you on 30th dec 1915, for which i return thanks. yours truly, 10760 Joseph Connolly connaught rangers stamped: 30 dec. 1915 please always give your regiment and regimental no. [printed] 'bureau de secours aux prissoniers de guerre section anglaise thunstrasse 50 berne suisse' [stamped 'gepruft'] [stamped '14 fev. 1916'] in a different hand? 'robert borel' in a different hand? 'j m dane esp.' no. 3237, joseph connolly 14th company zivilgen-fangenen lager, senne i sennelager die padeborn deutschland"
import os

gzfile = 'C:'+ os.sep + 'TestTexts' + os.sep + 'StanfordNER' + os.sep+'english.all.3class.nodistsim.crf.ser.gz'

jarfile = os.sep.join(['C:',
    'Users',
    'Rombli',
    'Downloads',
    'stanford-ner-2014-10-26',
    'stanford-ner-2014-10-26',
    'stanford-ner.jar'])



if os.path.exists(gzfile):
    print "loading gz file"

if os.path.exists(jarfile):
    print "loading jar file"

st = NERTagger(gzfile, jarfile)
l = st.tag(txt.split())








if __name__ == '__main__':
    pass
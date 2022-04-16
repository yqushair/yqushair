import os
import sys

for file in os.listdir('named_new_10ks/'):
    intro = "python ./basic_ner_test.py < ./named_new_10ks/"
    cmd = intro + file + " >> test.txt"
    os.system(cmd)

'''
Write a (Perl) program that generates the inverted index of a set of already preprocessed files. The files are stored in a directory which is given as an input parameter to the program. Use the files preprocessed in the previous assignment(s) as test data. Use raw term frequency (tf) in the document without normalizing it.

Think about saving the generated index, including the document frequency (df), in a file so that you can retrieve it later.
'''


import os
from collections import defaultdict

def inverted_index(source_directory,list_of_files):
    term_frequency = defaultdict(list)
    for file in list_of_files:
        temp_dict = {}
        with open(file, 'r', encoding="utf-8") as f:
            content = f.read()
            terms = content.split()
            terms_set=set(terms)
            processed_doc = file.replace(source_directory, '')
            for term in terms_set:
                if term.isalpha():
                    temp_dict[processed_doc] = terms.count(term)
                    term_frequency[term].append(temp_dict)
                    
    for term in term_frequency.keys():
        term_frequency[term].insert(0, len(term_frequency[term]))
    return term_frequency
            
    
    
source_directory="processed_files/"
list_of_files = os.listdir(source_directory)
processed_files = []
for file in list_of_files:
    if file.endswith(".txt"):
        file = source_directory + file
        processed_files.append(file)
result=inverted_index(source_directory,processed_files)      
        
with open("inverted_index.txt", 'w', encoding="utf-8") as f:
    for keys, values in sorted(result.items()):
        f.write(str(keys) + ' -----------> ' + str(values) + '\n \n') 
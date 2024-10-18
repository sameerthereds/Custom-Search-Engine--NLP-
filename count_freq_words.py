import os.path
from os import path
import requests
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
import re
def file_copy(sourcePath,destPath):
    if not path.exists(sourcePath):
        print("Source file not found")
    elif not sourcePath.endswith(".txt"):
        print("source file is not a text file")
    
    else:
        with open(sourcePath) as f:
            with open(destPath, "w") as f1:
                lines = f.readlines()
                print("File Copying started")
                for line in lines:
                    f1.write(line)
                print("File Copying done")
                
                


def count_words_URL(url):
    request = requests.get(url).text    
    soup = BeautifulSoup(request, 'html.parser').text  
    pre_processed_words = re.sub('[^A-Za-z]+', ' ', soup)  # regex to take only alphabet \    
    if "was not found on this server" in pre_processed_words:
        print("The requested URL "+str(url)+" was not found on this server.")
    else:
        freq_words = {}
        processed_words = pre_processed_words.lower().split()
        for word in processed_words:        
            if word not in freq_words:  
                freq_words[word] = 0
            freq_words[word] += 1

        print("Total number of words in the webpage : "+str(len(freq_words)))
        print("----------------------------------------------------------------")
        print("Alphabetical ordering of words with their frequencies")

        for key in sorted(freq_words.keys()):
            print("----------------")
            print(key, ":", freq_words[key])       
  



print("Problem - 1")
print("****************************************************************")
file_copy("source.txt","dest.txt")
print("****************************************************************")
print("Problem - 2")
print("****************************************************************")
count_words_URL("https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/")
print("****************************************************************")
import os.path
from os import path
import requests
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
import re
from collections import defaultdict
from pdfminer.high_level import extract_text
import io
from collections import Counter

"""
function to extract the text contents from a url given as input
"""


def getURL(url):
    try:
        response = requests.get(url)
        content = BeautifulSoup(response.text, 'html.parser').text
        filter_text = re.sub('[^A-Za-z]+', ' ', content)
        return filter_text
    except Exception as e:
        return ""
"""
function to extract the text contents from a url which contains text file given as input
"""
    
def getText(url):
    response = requests.get(url)
    content = response.text
    
    return content
"""
function to extract the text contents from a url which contains pdf file given as input
"""
def getPdf(url):    
    response = requests.get(url)
    text = extract_text(io.BytesIO(response.content))
   
    return text


"""
function to count  the words and create a dictionary
with the key as words and values as the their frequenices.
It also stores various documents a word has occured
"""
def count_words_URL(pre_processed_words,url):
    global dictionary_words
    try: 
        processed_words = str(pre_processed_words).split()
        for word in processed_words:  
            word = re.sub('[^A-Za-z]+', ' ',word)
            word=word.lower()
#             print(word)
            if word not in dictionary_words:  
                dictionary_words[word] = 0
            
            dictionary_words[word] += 1
            retrieved_texts[word].append(url)
    except Exception as e:
        pass
    
    
    
"""
Initialise global variables
"""
dictionary_words={}
retrieved_texts = defaultdict(list)
main_course_url="https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/"
count_words_URL(getURL(main_course_url),main_course_url) 
request = requests.get(main_course_url).text    
soup = BeautifulSoup(request, 'html.parser')

"""
Get all the external links from the page homepage
"""
urls=soup.findAll('a', href=True)
for link in urls:
    link = str(link.get('href'))
    if link.startswith('http') or link.endswith('.txt') or link.endswith('pdf'):
        if link.endswith('.txt'):
            links = main_course_url + link
            count_words_URL( getText(links),links)
        elif link.endswith('.pdf'):
            links = main_course_url + link
            count_words_URL( getPdf(links),links)
        else:
            if not "teaching/ir-websearch" in link:           
                count_words_URL( getURL(link),link) 
                

"""
Three dictionaries:
mod_retrieved_texts_count--> word : num of document it occured
mod_retrieved_texts_count_dict --> word: dictionary where 
document is a key and num of occurrences in each document
mod_retrieved_texts_docs --> word: set of documents it occured
"""
mod_retrieved_texts_count={}
mod_retrieved_texts_count_dict={}
mod_retrieved_texts_docs={}
for word in retrieved_texts:
    mod_retrieved_texts_count[word]=len(set(retrieved_texts[word]))
    mod_retrieved_texts_count_dict[word]=dict(Counter(retrieved_texts[word]))
    mod_retrieved_texts_docs[word]=(set(retrieved_texts[word]))

    
"""Sample Output"""
sample_word="retrieval"
print("****************************************************************")
print(" Sample word is: " + sample_word)
print("****************************************************************")
print("The Total frequency of "+ sample_word +" in the main page and other docs is : " + str(dictionary_words[sample_word]))
print("****************************************************************")
print(sample_word + " has occured in " + str(mod_retrieved_texts_count[sample_word]) + " different documents")
print("****************************************************************")
print(sample_word + " has occured in the following documents with the word frequency in each document")
print("****************************************************************")
for key, value in mod_retrieved_texts_count_dict[sample_word].items():
    print(key, ' : ', value)
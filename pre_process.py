"""
Problem 1 [30 points]. Write a Perl program that preprocesses a collection of documents using the recommendations given in the Text Operations lecture. The input to the program will be a directory containing a list of text files. Use the files from assignment #3 as test data as well as 10 documents (manually) collected from news.yahoo.com . The yahoo documents must be converted to text before using them. Remove the following during the preprocessing:

digits
punctuation
stop words (use the generic list available at ...ir-websearch/papers/english.stopwords.txt)
urls and other html-like strings
uppercases
morphological variations
"""

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
import re
import os

ps = PorterStemmer()

def remove_digits(txt):

    word_tokens = word_tokenize(txt)
    filtered_sentence=[]
    for word in word_tokens:
        if not word.isdigit():
            filtered_sentence.append(word)
   
    return " ".join(filtered_sentence)

def remove_puncs(txt):
    puncsets = set(punctuation)
    word_tokens = word_tokenize(txt)
    word_tokens=[word for word in word_tokens if word not in puncsets]    
    
    return " ".join(word_tokens)

def remove_stopwords(text):
    stop_words = stopwords.words("english")
    if not text in stop_words:
        return text
    
def lowercase(text):
    return text.lower()


def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", txt).split())

def stem(txt):    
    word_tokens = word_tokenize(txt) 
    word_tokens=[ps.stem(word) for word in word_tokens]    
    return " ".join(word_tokens)


def processing_file(file_content):
    file_content=lowercase(file_content)
    file_content=remove_url(file_content)
    file_content=remove_digits(file_content)
    file_content=remove_puncs(file_content)
    file_content=remove_stopwords(file_content)
    file_content=stem(file_content)
    
    return file_content


print("********************************************")
print("File reading and processing Started")
print("********************************************")

def main_function(input_test_directory,output_directory):
    input_test_directory="test_data"
    output_directory="processed_files"
    for file in os.listdir(input_test_directory):
        filepath = os.path.join(input_test_directory, file)
        if filepath.endswith(".txt"):
            try:

                with open(filepath, 'r') as reader:
                    file_content = reader.read()  

                    processed=processing_file(file_content)

            except:
                print("Something went wrong when reading the file" + file)
            destination_file = os.path.join(output_directory, "processed_"+file)
            try:
                with open(destination_file, 'w+') as reader:
                    reader.write(processed)
            except:
                print(" Something went wrong when writing the file " + file)
                
main_function("test_data","processed_files")
print("Processing and saving files completed")
print("********************************************")        
            
            
    
    
"""
This portion of code is to save the text files from the main course website to the input test directory
"""


# main_course_url="https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/"
# request = requests.get(main_course_url).text    
# soup = BeautifulSoup(request, 'html.parser')

# """
# Get all the external links from the page homepage
# """
# urls=soup.findAll('a', href=True)
# count=1
# for link in urls:
#     link = str(link.get('href'))
#     if link.startswith('http') or link.endswith('.txt') or link.endswith('pdf'):
#         if link.endswith('.txt'):
#             links = main_course_url + link
#             response = requests.get(links)
#             content = response.text
#             destination_file = os.path.join("test_data", "test_data_"+str(count))
#             count+=1
#             try:
#                 with open(destination_file, 'w+') as reader:
#                     reader.write(content)
#             except:
#                 print(" couldn't write to " + file)
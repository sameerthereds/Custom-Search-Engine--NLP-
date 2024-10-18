"""
Problem 1 : Automatically collect from memphis.edu 10,000 unique documents.The documents should be proper after converting them to txt (¿50 valid tokens after saved as text); only collect .html, .txt, and and .pdf web files and then convert them to text - make sure you do not keep any of the presentation tags such as html tags. You may use third party tools to convert the original files to text. Your output should be a set of 10,000 text files (not html, txt, or pdf docs) of at least 50 textual tokens each. You must write your own code to collect the documents - DO NOT use an existing crawler. Store for each proper file the original URL as you will need it later when displaying the results to the user.

"""



import requests
import re
import time
from bs4 import BeautifulSoup

counter = 0

list_of_links = []
dict_file={}
def removeTags(html):
    soup = BeautifulSoup(html, "html.parser")
  
    for data in soup(['style', 'script']):        
        data.decompose() 
   
    return ' '.join(soup.stripped_strings)

    

def getContent(pageUrl):
    content = ''
    try:
        request = requests.get(pageUrl)
        
        if ".pdf" in pageUrl:
            content = request.content
        else:
            content = request.text
    except Exception as e:
#         print(e)
        pass
    return content

def writeFile(url, filedir):
    
    global counter,dict_file,list_of_links
    
    content = getContent(url)
    increase_counter=False
    tokens=[]
    if url.endswith(".pdf"):
        tokens=content.split()
    else:
        content=removeTags(content)
        tokens=content.split()
    if len(tokens) > 50:
        increase_counter=True
    else:
        list_of_links.remove(url)
    if increase_counter:
        counter+= 1      
        dict_file[str(counter)]=url
        if url.endswith(".pdf"):
          # print(counter)
            file = filedir+str(counter)+'.txt'
            with open(file, 'wb') as f:
                f.write(content)
        else:
            content=removeTags(content)
            tokens=content.split()

            file = filedir+str(counter)+'.txt'
            with open(file, 'w', encoding='utf8') as f:
                f.write(content)
        
                
    

            
def crawler(url,filedir):
    
    global list_of_links, counter
    flag_pdf = False
    if url in list_of_links:        
        return
    list_of_links.append(url)
    if counter >= 10000:
        return   
      
       
    writeFile(url, filedir)
    if not url.endswith(".pdf"):
        content = getContent(url)
        links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', content)
        for link in links:
            if(str(link).find('memphis.edu')>=0):                
                crawler(link,filedir)
                
                
website_name="http://www.memphis.edu/"
def document_collection(website_name,filedir):
    crawler(website_name,filedir)    
    
document_collection(website_name,"input_files/")

count=1
with open("crawl_link.txt", 'w') as f:
        for item in list_of_links:
            f.write("{} : {}\n".format(count,item))
            count+=1




"""
Problem 2 [20 points]. Preprocess all the files using assignment #4. Save all preprocessed documents in a single directory which will be the input to the next assignment, index construction

"""


import re
import os
from bs4 import BeautifulSoup
import PyPDF2
from IR_assignment_4 import processing_file
def removeTags(html):
    soup = BeautifulSoup(html, "html.parser")
  
    for data in soup(['style', 'script']):        
        data.decompose() 
   
    return ' '.join(soup.stripped_strings)


def textProcessing(input_dir,file,output_dir):       
    with open(input_dir+file,'r',encoding='utf-8') as f:
        content = f.read()
    content=removeTags(content)
    content = processing_file(content)
    return content
    
def pdfProcessing(input_dir,file,output_dir):
    pdf = PyPDF2.PdfFileReader(open(input_dir+file, "rb"))
    for i in range(0, pdf.getNumPages()):
        content= pdf.getPage(i).extractText() + "\n"
    content = processing_file(content)
    return content

def file_processing(input_dir,output_dir):
    
    input_files = os.listdir(input_dir)
    for file in input_files:
        if(".txt" in file):
           
            content=textProcessing(input_dir,file,output_dir)
            filename = os.path.join(output_dir,file)
            with open(filename,'w',encoding = 'utf-8') as f:
                f.write("%s\n" % content)

        if (".pdf" in file):
            content=pdfProcessing(input_dir,file,output_dir)
            filename = os.path.join(output_dir, file.replace('.pdf','.txt'))
            with open(filename, 'w',encoding='utf-8') as f:
                f.write("%s\n" % content)

file_processing("input_files/","preprocessed_files/")  

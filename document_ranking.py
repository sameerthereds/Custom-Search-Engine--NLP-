import pickle
import math


def documents_ranking(processed_query):   
    matched_documents = {}
    list_of_links=[]
    sorted_ranked_documents=[]
    query_tokens = processed_query.split()
    query_w=[]
    if len(query_tokens) > 0:
        for token in query_tokens:
            # get count of token in the query
            count=query_tokens.count(token)                   
            document_retrieval(token,query_w,count,matched_documents)      
    
    temp=0
    print(query_w)
    for w in query_w:
        temp+=math.pow(w,2)
    #calculate the square root of swaures of its weights
    query_normalised=math.sqrt(temp)
    
    normalised_matched_documents={}
    document_length=0
    if len(matched_documents) >0:
        for doc in matched_documents:          
            with open("preprocessed_files/"+doc) as f:
                lines=f.read()
                tokens=lines.split()
                document_length=len(tokens)
            # normalise the final similarity scores
            normalised_matched_documents[doc]=matched_documents[doc]/(query_normalised*document_length)
    if len(normalised_matched_documents)>0:  
        with open("crawl_link.txt") as f:
            lines=f.readlines()
        #retreive the top 10 sorted documents
        sorted_ranked_documents = sorted(normalised_matched_documents.items(), key=lambda x: x[1], reverse=True)[:10]
        print(*[i[0] for i in sorted_ranked_documents],sep='\n')        
        for file in sorted_ranked_documents:
            file_number=file[0].split(".")[0]
            for line in lines:
                if len(line)>0:
                    temp=line.split(" :")
                    if temp[0] == file_number:

                        list_of_links.append((temp[1]))
        return list_of_links
    else:
        return list_of_links


def document_retrieval(token,query_w,count,matched_documents):
    highest_frequency = 0
    with open('inverted_index.pickle', 'rb') as inverted_index:
        inverted_index_mappings = pickle.load(inverted_index)
    # get all the keys from the inverted index
    inverted_index = inverted_index_mappings.keys()  
    #get document frequency
    document_frequency = inverted_index_mappings[token][0] 
    # get IDF of token 
    q_idf=math.log(10000 / document_frequency,2) 
    # calculate the weight of T
    w_q=count*q_idf
    query_w.append(w_q)
    if token not in inverted_index:
        return "Cound not find any documents related to the query"
    # get highest document frequency of token in inverted index
    for documents in inverted_index_mappings[token]:
        if type(documents) is dict:            
            if highest_frequency < int(list(documents.values())[0]):
                highest_frequency = int(list(documents.values())[0])
    for documents in inverted_index_mappings[token]:
        if  type(documents) is dict:
            # get cosine similarity
            cosine_similarity(documents,w_q, highest_frequency, document_frequency,matched_documents)
    

def cosine_similarity(document, w_q,highest_frequency, document_frequency,matched_documents):
    document_length = 0
    total_documents = 10000
    query_length = 1
    # get term frequency
    term_frequency = int(list(document.values())[0]) / int(highest_frequency)  
    # get the inverse document frequency
    inverse_document_frequency = math.log(total_documents / document_frequency,2)  
    #calculate the similarity
    similarity = (w_q*term_frequency * inverse_document_frequency)
    search_document = list(document.keys())[0]
    if search_document in matched_documents:
        matched_documents[search_document] = matched_documents[search_document] + similarity
    else:
        matched_documents[search_document] = similarity 
    return matched_documents
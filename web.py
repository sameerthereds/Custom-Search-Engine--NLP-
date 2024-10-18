from flask import Flask, render_template, request
from IR_assignment_4 import processing_file
import document_ranking as ranking
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/results", methods=['GET', 'POST'])
def results():
    
    query = request.form['query']
    orig_query=query
    #preprocess the query
    processed_query = processing_file(query)

    # send the processed query to the document_ranking function to retrieve the relevant documents   
    list_of_links = ranking.documents_ranking(processed_query)
    return render_template('results.html', query=processed_query, orig_query=orig_query, links=list_of_links)
    

if __name__ == "__main__":
    app.run()

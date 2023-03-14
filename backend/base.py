from flask import Flask
from flask import request
import pandas as pd
from utils.string_transforms import string_to_list
import json
import pickle 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#load the nlp model and the tfid vect 
nlp_model = 'models/nlo_model.pkl'
#open the file in binary format: read

#function for similairty
def create_similarity():
    data = pd.read_csv("final_data/new_moviedata.csv")
    #create the count matrix as cv
    cv = CountVectorizer()
    #create the matrix based on the column comb which is the combination of them all 
    count_matrix = cv.fit_transform(data['comb'])
    #create the similiaity score matrix 
    similarity = cosine_similarity(count_matrix)
    return data, similarity 


api = Flask(__name__)

@api.route('/search-prod-info')
def search_prod_info():

    movie_data = pd.read_csv("final_data/new_moviedata.csv")
    movie_score = pd.read_csv("final_data/movie_score.csv")

    query = request.args.get('query', default=None, type=str)
    
    #Since everything in the dataframe is a float, we have this stupid solution
    if(query.isdigit()):
        query+=".0"

    response_body = {
        'movie_data': {
            'movie_title': [],
            "director_name": [],
            "genres": [],
        },
        'movie_score': {
            'release': []
        }
    }
    
    for column_name in response_body['movie_data']:
        data = movie_data.loc[movie_data[column_name].astype(str).str.lower()==query.lower()]
        if not(data.empty):
            for key in response_body['movie_data']:
                response_body['movie_data'][key].extend(data[key].to_list())

    final_body = json.dumps({
        'title': response_body['movie_data']['movie_title'][0],
        'director': response_body['movie_data']['director_name'][0],
        'genres': response_body['movie_data']['genres'],
        'year': 'TEMP'
    })

    print(final_body)

    return final_body
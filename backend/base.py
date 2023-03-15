from flask import Flask
from flask import request
import pandas as pd
from utils.string_transforms import string_to_list
import json
import pickle 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 

#load the nlp model and the tfid vect 
nlp_model = 'models/nlp_model.pkl'
#open the file in binary format: read
clf = pickle.load(open(filename, 'rb'))
vect = pickle.load(open('transform.pkl', 'rb'))

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

#recommendation function-> rec
def rec(m): #movies -> m
    m = m.lower() #make the movies lowercase 
    try: #test below for errors/ handles them
        data.head()
        similarity.shape
    except: 
        data, similarity = create_similarity()
    #if the movie title is not there, then return sorry :(
    if m not in data['movie_title'].unique(): 
        return('The movie you requested is not in our database, sorry!')
    else: 
        #now when movie is found
        i = data.loc[data['movie_title']==m].index[0]
        m_list = list(enumerate(similarity[i]))
        m_list = sorted(m_list, key = lambda x:x[1], reverse = True)
        #the list is ten movies but we exclude the first itme since it is the one being requested
        m_list = m_list[1:11]
        #create empty array to add the movie titles 
        l = []
        for i in range(len(list)):
            u =m_list[i][0]
            l.append(data['movie_title'][u])
        return l 

#convert list of string to just a list -> ["abc", "def"]
def convert_to_list(my_list):
    my_list = my_list.split(' ","') 
    #replacing the brackets []
    my_list[0] = my_list[0].replace('["', '')
    my_list[-1] = my_list[-1].replace('"]', '')
    return my_list

# def get_suggestions():
#     datat = pd.read_csv("final_data/new_moviedata.csv")
#     return list(data['movie_title'].str.capitalize()) #return movies with titles capitalized 

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
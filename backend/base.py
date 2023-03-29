from flask import Flask
from flask import request
import pandas as pd
import json
import pickle 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
import requests  
import os

#load the nlp model and the tfid vect 
nlp_model = 'models/nlp_model.pkl'
#open the file in binary format: read
clf = pickle.load(open(nlp_model, 'rb'))
vect = pickle.load(open('models/transform.pkl', 'rb'))

#function for similairty
def create_similarity(data):
    #create the count matrix as cv
    cv = CountVectorizer()
    #create the matrix based on the column comb which is the combination of them all 
    count_matrix = cv.fit_transform(data['all'].values.astype('U'))
    #create the similiaity score matrix 
    similarity = cosine_similarity(count_matrix)
    return data, similarity 

#recommendation function-> rec
def rec(m, data): #movies -> m
    m = m.lower() #make the movies lowercase 
    data, similarity = create_similarity(data)
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
        for i in range(len(m_list)):
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
#     data = pd.read_csv("final_data/new_moviedata.csv")
#     return list(data['movie_title'].str.capitalize()) #return movies with titles capitalized 

api = Flask(__name__)

TMDB_API_KEY = "21742194230c942f4f9ca9b6b7e27659"
API_KEY = os.environ.get("TMDB_API_KEY")

if API_KEY is None:
    print("API_KEY environment variable is not set.")
    exit()

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
            "overview": [],
            "poster_path": [],
            "streaming_services": []
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


    #call tmdb api to retrieve the additional movie information - streaming services 
    response = requests.get(f"https://api.themoviedb.org/3/movie/550?api_key={API_KEY}&query={query}")
    results = response.json().get('results')

    if results:
        tmdb_movie = results[0]

        #add overview poster and release data to the body 
        response_body['movie_data']['overview'] = tmdb_movie.get('overview', '')
        response_body['movie_data']['poster_path'] = tmdb_movie.get('poster_path', '')
        response_body['movie_data']['release'] = tmdb_movie.get('release_date', '')

    # movie_info_extra = pd.read_csv('data/movies_metadata.csv')
    # release_date = movie_info_extra.loc[movie_info_extra['original_title'].astype(str).str.lower() == response_body['movie_data']['movie_title'][0]]
   
        #call the tmdb api to get the atreaming services available
        response = requests.get(f"https://api.themoviedb.org/3/movie/{tmdb_movie['id']}/watch/providers?api_key={API_KEY}")
        providers = response.json().get('results', {}).get('US', {}).get('flatrate', [])

        #add streaming services to the response body 
        response_body['movie_data']['streaming_services'] = [provider.get('provider_name', '') for provider in providers]


    similar_films = rec(response_body['movie_data']['movie_title'][0], movie_data)

    final_body = json.dumps({
        'title': response_body['movie_data']['movie_title'][0],
        'director': response_body['movie_data']['director_name'][0],
        'genres': response_body['movie_data']['genres'],
        'overview': response_body['movie_data']['overview'],
        'poster_path': response_body['movie_data']['poster_path'],
        'year': response_body['movie_score']['release'],
        'streaming_services': response_body['movie_data']['streaming_services'],
        'similar': similar_films
    })

    return final_body

@api.route('/get-page')
def get_page():
    
    page_num = request.args.get('page_num', type=int)
    page_length = int(request.args['page_length'])

    movie_data = pd.read_csv("final_data/new_moviedata.csv")

    total_pages = len(movie_data)/page_length

    print(page_num)

    #Make sure page num is within the max pages
    if(page_num>total_pages):
        page_num = int(total_pages-1)

    start_index = page_length*page_num
    end_index = (page_length*page_num)+page_length

    titles = movie_data['movie_title'].values.tolist()
    for index, title in enumerate(titles):
        titles[index] = title.title()

    page_titles = titles[start_index:end_index]

    response_body = json.dumps({
        'titles': page_titles
    })

    return response_body
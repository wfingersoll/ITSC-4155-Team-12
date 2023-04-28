#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing the required libraries
import numpy as np
import pandas as pd
import pickle
#import matrix_factorization 
import scipy.sparse as sp
from scipy.sparse.linalg import svds


# In[2]:


#pip install scipy


# In[3]:


#read in the ratings data
ratings = pd.read_csv("./data/ratings_small.csv")


# In[4]:


len(ratings)


# In[5]:


#only takig three columns userId, movieID and rating into the df
ratings = ratings[['userId', 'movieId','rating']]


# In[6]:


#need to check if the user has multiple ratings for a movie because if so we can just condense them to be the max
#using np.max
ratings


# In[7]:


#need to check if the user has multiple ratings for a movie because if so we can just condense them to be the max
#using np.max
ratings_df = ratings.groupby(['userId','movieId']).aggregate(np.max)


# In[8]:


#lets print out the length to see if there were any changes, ofcourse it will be left after aggregating
len(ratings_df)


# In[9]:


#we see that the length is the same as before, so no user has made a review more than once on a movie
#lets move on in inspecting the ratings data a bit further


# In[10]:


#first five
ratings.head()


# In[11]:


ratings_df.head()


# In[12]:


#see how many unique ids there are 
len(ratings['userId'].unique())


# In[13]:


#get the percentage of each rating value
#first get the number of each rating and then divide by the total
count_ratings = ratings.groupby('rating').count()
#create a new column per_total 
count_ratings['per_total']=round(count_ratings['userId']*100/count_ratings['userId'].sum(),1)


# In[14]:


count_ratings


# In[15]:


#use ply plot.bar the to visualize the per total using a bar graph
count_ratings['per_total'].plot.bar()


# In[16]:


#now lets read in the movies dataset
movie_list = pd.read_csv("./final_data/movie_score.csv")


# In[17]:


len(movie_list)


# In[18]:


#lets see the file
movie_list.head()


# In[19]:


#no lets read the tags intnto tags df 
tags = pd.read_csv("./data/tags.csv")


# In[20]:


#lets see the file
tags.head()


# In[21]:


#create a genres_df of the column genres from the movie_list df
genres = movie_list['genres']


# In[22]:


genres.head()


# In[23]:


#cleaning
#we see that the genres are formatted using | to sepearate the generes so we will split the genres from them and create
#a new list based on the split genres into new_list and then remove the blank 


# In[24]:


genre_list = ""
for index,row in movie_list.iterrows():
        genre_list += row.genres + "|"
#split the string into a list of values
genre_list_split = genre_list.split('|')
#de-duplicate values
new_list = list(set(genre_list_split))
#remove the value that is blank
new_list.remove('')
#let's see it now
new_list


# In[25]:


#lets add the generes into their own columns using .copy on the movie_list
movies_with_genres = movie_list.copy()


# In[26]:


for genre in new_list :
    movies_with_genres[genre] = movies_with_genres.apply(lambda _:int(genre in _.genres), axis = 1)

movies_with_genres.head() #df with new columns with generes


# In[27]:


#lets check the sparisty by taking the length of the ratings divided by the unique no of users and number of movies
num_users = len(ratings['userId'].unique())
num_movies = len(ratings['movieId'].unique())


# In[28]:


sparsity = round(1.0 - len(ratings)/(1.0*(num_movies*num_users)),3)
print(sparsity)


# In[29]:


#count the number of unique elements in movieID
len(ratings['movieId'].unique())


# In[30]:


#now we will find the average rating for a movie and then the number of ratings for each movie 
#so can use aggregate function .agg for the average/mean of a rating and the count
avg_movie_rating = pd.DataFrame(ratings.groupby('movieId')['rating'].agg(['mean','count']))


# In[31]:


# avg_movie_rating['movieId']= avg_movie_rating.index


# In[32]:


#lets see
avg_movie_rating.head()


# In[33]:


len(avg_movie_rating)


# In[34]:


#calculate the percentile count
np.percentile(avg_movie_rating['count'],60)


# In[35]:


#the average movie rating for all movies 
avg_rating_all=ratings['rating'].mean()
avg_rating_all


# In[36]:


#set a minimum threshold for number of reviews that the movie has to have
min_reviews=30 #30 is reasonable
min_reviews


# In[37]:


movie_score = avg_movie_rating.loc[avg_movie_rating['count']>min_reviews]
movie_score.head()


# In[38]:


len(movie_score)


# In[39]:


#create a function for weighted rating score based off the count of reviews
def weighted_rating(x, m=min_reviews, C=avg_rating_all):
    v = x['count']
    R = x['mean']
    # formula based on the IMDB formula 
    #= votes/cotes + minimum votes required to be on top 50 * average of the movie so the mean, ratings
    # + the minm votes / minm votes + votes * the mean votes acorss the whole
    
    return (v/(v+m) * R) + (m/(m+v) * C)


# In[40]:


#now we should calculate the weighted score for each movie
movie_score['weighted_score'] = movie_score.apply(weighted_rating, axis=1)
movie_score.head()


# In[41]:


#join movie details to movie ratings
movies_with_genres.index.name = None #.drop(columns=[])#, axis = 1)
movies_with_genres = movies_with_genres.rename_axis(None) 
movie_score = pd.merge(movie_score,movies_with_genres,on='movieId')
#movie_score = movie_score.index.name = NULL
#join movie links to movie ratings
#movie_score = pd.merge(movie_score,links,on='movieId')
movie_score.head()


# In[42]:


#now lets list the top scored movies over the whole range of movies
print(movie_score.head())
pd.DataFrame(movie_score.sort_values(['weighted_score_x'],ascending=False)[['title','count_x','mean_x','weighted_score_x','genres']][:10])


# In[43]:


#create best movies by genre based on weighted score which is calculated using IMDB formula we used above
def best_movies_by_genre(genre,top_n):
    return pd.DataFrame(movie_score.loc[(movie_score[genre]==1)].sort_values(['weighted_score_x'],ascending=False)[['title','count_x','mean_x','weighted_score_x']][:top_n])


# In[142]:


movie_score.to_csv('movie_score.csv',index=False)


# In[44]:


#call the function to return top recommended movies by genre, here musical
best_movies_by_genre('Musical',10)  


# In[45]:


#do the same, call function to return top recommended movies by genre, action
best_movies_by_genre('Action',10)  


# In[46]:


#now call th efunction to return top recommended movies by genre, children
best_movies_by_genre('Children',10)  


# In[47]:


#run function to return top recommended movies by genre, drama
best_movies_by_genre('Drama',10)  


# In[48]:


#lets create a data frame that contains the user ratings accross all movies in form of matrix used in matrix factorisation
ratings_df = pd.pivot_table(ratings, index='userId', columns='movieId', aggfunc=np.max)


# In[49]:


#lets see it 
ratings_df.head()


# In[50]:


#import matrix_factorization


# In[51]:


#pip install matrix-factorization


# In[52]:


#apply low rank matrix factorization to find the latent features 
#U, M = matrix_factorization.low_rank_matrix_factorization(ratings_df.as_matrix(),num_features=5,regularization_amount=1.0)

#lets proceed wihtout doing this


# In[53]:


ratings_df


# In[54]:


#merging ratings and movies dataframes
ratings_movies = pd.merge(ratings,movie_list, on = 'movieId')


# In[55]:


ratings_movies.head()


# In[56]:


ratings_movies


# In[57]:


#lets define a function that will return/show the other top ten movies which are watched by the people who saw this particular movie
def get_other_movies(movie_name):
    #get all users who watched a specific movie were title = user id
    df_movie_users_series = ratings_movies.loc[ratings_movies['title']==movie_name]['userId']
    #convert to a data frame
    df_movie_users = pd.DataFrame(df_movie_users_series,columns=['userId'])
    #now get a list of all other movies watched by these users
    other_movies = pd.merge(df_movie_users,ratings_movies,on='userId')
    #get a list of the most 'commonly' watched movies by these other user
    other_users_watched = pd.DataFrame(other_movies.groupby('title')['userId'].count()).sort_values('userId',ascending=False)
    #get the percentage of those who watched
    other_users_watched['per_who_watched'] = round(other_users_watched['userId']*100/other_users_watched['userId'][0],1)
    #return the top ten
    return other_users_watched[:10]


# In[59]:


#now that we have it working, lets continue


# In[60]:


from sklearn.neighbors import NearestNeighbors


# In[61]:


avg_movie_rating.head()


# In[62]:


#only include movies with more than ten ratings
movie_more_10_ratings = avg_movie_rating.loc[avg_movie_rating['count']>=10]
#print the number of those movies with more than ten ratings
print(len(movie_more_10_ratings))


# In[63]:


movie_more_10_ratings


# In[64]:


#combind the df based on movie ids
filtered_ratings = pd.merge(movie_more_10_ratings, ratings, on="movieId")
len(filtered_ratings)


# In[65]:


#thats a lot


# In[66]:


filtered_ratings.head()


# In[67]:


#now lets create a matrix table with movie idds on the rows and user ids on the columns
movie_wide = filtered_ratings.pivot(index = 'movieId', columns = 'userId', values = 'rating')
movie_wide.head()


# In[68]:


#we see a lot of nan, lets replace that with 0 
movie_wide = filtered_ratings.pivot(index = 'movieId', columns = 'userId', values = 'rating').fillna(0)
movie_wide


# In[69]:


#now lets begin to specify the models parameters
knn = NearestNeighbors(metric='cosine',algorithm='brute')
#fit model to the data set we just worked with 
knn.fit(movie_wide)


# In[70]:


#define a function that returns the top ten nearest neighbours of the movie
def similar_movies(query_index) :
    #get the list of user ratings based on a user id, need to reshape to fit the matrix 
    query_index_movie_ratings = movie_wide.loc[query_index,:].values.reshape(1,-1)
    #get the closest te movies and their distances from the movie specified
    distances,indices = knn.kneighbors(query_index_movie_ratings,n_neighbors = 11) 
    #create a loop that prints the similar movies for a specified movie.
    for i in range(0,len(distances.flatten())):
        #get the title of the random movie that was chosen
        get_movie = movie_list.loc[movie_list['movieId']==query_index]['title']
        #since the first movie is the close should specify it more,  print the title
        if i==0:
            print('Recommendations for {0}:\n'.format(get_movie))
        else :
            #get the indiciees for the closest movies
            indices_flat = indices.flatten()[i]
            #get the title of the movie
            get_movie = movie_list.loc[movie_list['movieId']==movie_wide.iloc[indices_flat,:].name]['title']
            #print the movie
            print('{0}: {1}, with distance of {2}:'.format(i,get_movie,distances.flatten()[i]))


# In[71]:


#lets see with a random index
similar_movies(10)


# In[72]:


#lets see with a random index
similar_movies(101)


# In[73]:


similar_movies(1009)


# In[74]:


similar_movies(96079)


# In[75]:


movies_with_genres.head()


# In[76]:


#get the movies list with only a sepcific genre and other columns that are needed for context
movie_content_df_temp = movies_with_genres.copy()
movie_content_df_temp.set_index('movieId')
movie_content_df = movie_content_df_temp.drop(columns = ['movieId','title','genres'])
#movie_content_df = movie_content_df.as_matrix()
movie_content_df


# In[77]:


#now based on content


# In[78]:


from sklearn.metrics.pairwise import linear_kernel


# In[79]:


#cmpute the cosine similarity matrix linear based on the content
cosine_sim = linear_kernel(movie_content_df,movie_content_df)


# In[80]:


#so cosince_sum is similaritly of the movies based on the content
cosine_sim


# In[81]:


#create a series of the movie id and title
indicies = pd.Series(movie_content_df_temp.index, movie_content_df_temp['title'])
indicies 


# In[82]:


#now lets get the top ten similar movies based on the content
def get_similar_movies_based_on_content(movie_index) :
    sim_scores = list(enumerate(cosine_sim[movie_index]))
    #sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    #getthe scores of the ten most similar moviesusing 0 - 11
    sim_scores = sim_scores[0:11]
    #print those ten socres
    print(sim_scores)
    #now get the movie title based on the movie indices
    movie_indices = [i[0] for i in sim_scores]
    #print them
    print(movie_indices)
    similar_movies = pd.DataFrame(movie_content_df_temp[['title','genres']].iloc[movie_indices])
    return similar_movies


# In[83]:


#lets try with a movie to see if we get the indicies
indicies["Skyfall (2012)"]


# In[84]:


indicies["Jumanji (1995)"]


# In[85]:


#now lets call the function given a index
get_similar_movies_based_on_content(14)


# In[86]:


#so were we are given a list of indices and then the
#title of those movies with respect to those indices


# In[87]:


get_similar_movies_based_on_content(1444)


# In[88]:


#now get the ordered list of movie ids
item_indices = pd.DataFrame(sorted(list(set(ratings['movieId']))),columns=['movieId'])
#add the data frame index value to data frame
item_indices['movie_index']=item_indices.index
#lets see it now
item_indices.head()


# In[89]:


#now the index and movie id are together


# In[90]:


#now have to do the same now for the user incdices, get ordered list of movieIds
user_indices = pd.DataFrame(sorted(list(set(ratings['userId']))),columns=['userId'])
#add in data frame index value to data frame
user_indices['user_index']=user_indices.index
user_indices.head()


# In[91]:


#now lets join the movie indices
df_with_index = pd.merge(ratings,item_indices,on='movieId')
#then oin the user indices
df_with_index=pd.merge(df_with_index,user_indices,on='userId')
#lets see it
df_with_index.head()


# In[92]:


#so now we have the user id, movie id and ratings and their repsected incidieces in one


# In[93]:


#now lets beign training/testing 
from sklearn.model_selection import train_test_split


# In[94]:


#do 20/80 80 on training and  20 as tesst set
df_train, df_test= train_test_split(df_with_index,test_size=0.2)
print(len(df_train))
print(len(df_test))


# In[95]:


df_train.head()


# In[96]:


df_test.head()


# In[97]:


#get the number of unique user ids and movie ids
n_users = ratings.userId.unique().shape[0]
n_items = ratings.movieId.unique().shape[0]
print(n_users)
print(n_items)


# In[98]:


#create two user x item matrices
#one will be for training and the other for testing
train_data_matrix = np.zeros((n_users, n_items))
    #for lop to go through every line in the data
for line in df_train.itertuples():
    #set the rows to the column names, userid, movieid, rating, movie index and user index as 0,1,2,3,4
    #traing it based on movie and user index on rating
    train_data_matrix[line[5], line[4]] = line[3]
train_data_matrix.shape


# In[99]:


#now do the saem for the test 
test_data_matrix = np.zeros((n_users, n_items))
    #for every line in the data
for line in df_test[:1].itertuples():
    test_data_matrix[line[5], line[4]] = line[3]
test_data_matrix.shape


# In[100]:


#this means that the same of the matrix should be the size of the user ids and movie ids


# In[101]:


pd.DataFrame(train_data_matrix).head()


# In[102]:


#see what the max rating is in the trianing set
df_train['rating'].max()


# In[103]:


from sklearn.metrics import mean_squared_error
from math import sqrt
#define rmse to see how well the model is doing so far
def rmse(prediction, ground_truth): #use root mean square error 
    #select prediction values that are not zero and flatten into 1 array
    prediction = prediction[ground_truth.nonzero()].flatten() 
    #select test values that are not zero and flatten into 1 array
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()
    #return RMSE between values which is the difference between truth and pred 
    return sqrt(mean_squared_error(prediction, ground_truth))


# In[104]:


#now lets calculate the rmse sscore of svd using different values of k, since k is a hyperparameter
rmse_list = []
for i in [1,2,5,20,40,60,100,200]:
    #apply svd to the test data
    u,s,vt = svds(train_data_matrix,k=i)
    #get diagonal matrix
    s_diag_matrix=np.diag(s)
    #predict x with dot product of u s_diag and vt
    X_pred = np.dot(np.dot(u,s_diag_matrix),vt)
    #calculate rmse score of matrix factorisation predictions
    rmse_score = rmse(X_pred,test_data_matrix)
    rmse_list.append(rmse_score)
    print("Matrix Factorisation with " + str(i) +" latent features has a RMSE of " + str(rmse_score))


# In[105]:


#now cover the predictions, X_pred to a df 
mf_pred = pd.DataFrame(X_pred)
mf_pred.head()


# In[106]:


#lets merge the ratings and movie list df based on the movie ids
df_names = pd.merge(ratings,movie_list,on='movieId')
#lets check
df_names.head()


# In[107]:


#choose a user id
user_id = 1
#get movies rated by this user id
users_movies = df_names.loc[df_names["userId"]==user_id]
#print how many ratings user has made 
print("User ID: " + str(user_id) + ", has rated " + str(len(users_movies)) + " movies")
#list movies that have been rated
users_movies


# In[108]:


user_index = df_train.loc[df_train["userId"]==user_id]['user_index'][:1].values[0]
#get movie ratings predicted for this user and sort by the highest rating prediction
sorted_user_predictions = pd.DataFrame(mf_pred.iloc[user_index].sort_values(ascending=False))
#rename the columns to ratings
sorted_user_predictions.columns=['ratings']
#save the index values as movie id
sorted_user_predictions['movieId']=sorted_user_predictions.index
print("Top 10 Predictions for User " + str(user_id))
#display the top ten predictions for this user
pd.merge(sorted_user_predictions,movie_list, on = 'movieId')[:10]


# In[109]:


#lets count the nnumber of unique users
numUsers = df_train.userId.unique().shape[0]
#and then count number of unique movies
numMovies = df_train.movieId.unique().shape[0]
print(len(df_train))
print(numUsers) 
print(numMovies) 


# In[110]:


#now lets separate out the values of the training data set into separate variables
Users = df_train['userId'].values
Movies = df_train['movieId'].values
Ratings = df_train['rating'].values


# In[111]:


print(Users),print(len(Users))
print(Movies),print(len(Movies))
print(Ratings),print(len(Ratings))


# In[112]:


import keras


# In[113]:


#import necessarity libraries from keras
from keras.layers import Embedding, Reshape
from keras.layers import Concatenate
from keras.models import Sequential
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.utils import plot_model


# In[114]:


#count the number of unique users and movies
len(ratings.userId.unique()), len(ratings.movieId.unique())


# In[115]:


#assign a unique value to each user and movie in range 0 to the number of users and do the saem for movies respectively.
ratings.userId = ratings.userId.astype('category').cat.codes.values
ratings.movieId = ratings.movieId.astype('category').cat.codes.values


# In[116]:


#now split the data into train and test 80/20
train, test = train_test_split(ratings, test_size=0.2)


# In[117]:


train.head()


# In[118]:


test.head()


# In[119]:


n_users, n_movies = len(ratings.userId.unique()), len(ratings.movieId.unique())


# In[123]:


from keras.layers import dot


# In[124]:


#define a nn model whicch performs matrix factorisation
def matrix_fac_model(n_latent_factors) :
    movie_input = keras.layers.Input(shape=[1],name='Item')
    movie_embedding = keras.layers.Embedding(n_movies + 1, n_latent_factors, name='Movie-Embedding')(movie_input)
    movie_vec = keras.layers.Flatten(name='FlattenMovies')(movie_embedding)

    user_input = keras.layers.Input(shape=[1],name='User')
    user_vec = keras.layers.Flatten(name='FlattenUsers')(keras.layers.Embedding(n_users + 1, n_latent_factors,name='User-Embedding')(user_input))
    prod = dot([movie_vec, user_vec],axes =1, normalize = False)
    
    model = keras.Model([user_input, movie_input], prod)
    model.compile('adam', 'mean_squared_error')
    
    return model


# In[125]:


model = matrix_fac_model(5)


# In[126]:


model.summary()


# In[132]:


import timeit


# In[133]:


#want to time how long it takes
start_time = timeit.default_timer()
#train the model
history = model.fit([train.userId, train.movieId], train.rating, epochs=50, verbose=0)
elapsed = timeit.default_timer() - start_time


# In[134]:


#y_hat is the prediction and y_true ais the actual
y_hat = np.round(model.predict([test.userId, test.movieId]),0)
y_true = test.rating


# In[135]:


from sklearn.metrics import mean_absolute_error
#use mse to check out the error
mean_absolute_error(y_true, y_hat)


# In[137]:


#get the summary of movie embeddings
movie_embedding_learnt = model.get_layer(name='Movie-Embedding').get_weights()[0]
pd.DataFrame(movie_embedding_learnt).describe()


# In[138]:


#now get the summary of user embeddings from the model
user_embedding_learnt = model.get_layer(name='User-Embedding').get_weights()[0]
pd.DataFrame(user_embedding_learnt).describe()


# In[143]:


from keras.constraints import non_neg


# In[144]:


#lets train another model, return a neural network model which performs matrix factorisation with additional constraint on embeddings that they can't be negative
def matrix_fact_nn(n_latent_factors) :
    movie_input = keras.layers.Input(shape=[1],name='Item')
    movie_embedding = keras.layers.Embedding(n_movies + 1, n_latent_factors, name='Non-Negative-Movie-Embedding',embeddings_constraint=non_neg())(movie_input)
    movie_vec = keras.layers.Flatten(name='FlattenMovies')(movie_embedding)

    user_input = keras.layers.Input(shape=[1],name='User')
    user_vec = keras.layers.Flatten(name='FlattenUsers')(keras.layers.Embedding(n_users + 1, n_latent_factors,name='Non-Negative-User-Embedding',embeddings_constraint=non_neg())(user_input))
    prod = dot([movie_vec, user_vec],axes =1, normalize = False)
    
    model = keras.Model([user_input, movie_input], prod)
    model.compile('adam', 'mean_squared_error')
    
    return model


# In[145]:


model2 = matrix_fact_nn(5)


# In[146]:


model2.summary()


# In[147]:


start_time = timeit.default_timer()
history_nonneg = model2.fit([train.userId, train.movieId], train.rating, epochs=50, verbose=0)
elapsed = timeit.default_timer() - start_time


# In[148]:


movie_embedding_learnt = model2.get_layer(name='Non-Negative-Movie-Embedding').get_weights()[0]
pd.DataFrame(movie_embedding_learnt).describe()


# In[149]:


y_hat = np.round(model2.predict([test.userId, test.movieId]),0)
y_true = test.rating


# In[150]:


mean_absolute_error(y_true, y_hat)


# In[151]:


#lower error


# In[152]:


#return a neural network model which does the recommendation
def nn_model(n_latent_factors_user, n_latent_factors_movie):
    
    movie_input = keras.layers.Input(shape=[1],name='Item')
    movie_embedding = keras.layers.Embedding(n_movies + 1, n_latent_factors_movie, name='Movie-Embedding')(movie_input)
    movie_vec = keras.layers.Flatten(name='FlattenMovies')(movie_embedding)
    movie_vec = keras.layers.Dropout(0.2)(movie_vec)


    user_input = keras.layers.Input(shape=[1],name='User')
    user_vec = keras.layers.Flatten(name='FlattenUsers')(keras.layers.Embedding(n_users + 1, n_latent_factors_user,name='User-Embedding')(user_input))
    user_vec = keras.layers.Dropout(0.2)(user_vec)


    concat = keras.layers.Concatenate()([movie_vec, user_vec])
    concat_dropout = keras.layers.Dropout(0.2)(concat)
    dense = keras.layers.Dense(100,name='FullyConnected')(concat)
    dropout_1 = keras.layers.Dropout(0.2,name='Dropout')(dense)
    dense_2 = keras.layers.Dense(50,name='FullyConnected-1')(concat)
    dropout_2 = keras.layers.Dropout(0.2,name='Dropout')(dense_2)
    dense_3 = keras.layers.Dense(20,name='FullyConnected-2')(dense_2)
    dropout_3 = keras.layers.Dropout(0.2,name='Dropout')(dense_3)
    dense_4 = keras.layers.Dense(10,name='FullyConnected-3', activation='relu')(dense_3)


    result = keras.layers.Dense(1, activation='relu',name='Activation')(dense_4)
    adam = Adam(lr=0.005)
    model = keras.Model([user_input, movie_input], result)
    model.compile(optimizer=adam,loss= 'mean_absolute_error')
    return model


# In[153]:


model3 = nn_model(10,13)


# In[154]:


start_time = timeit.default_timer()
history_neural_network = model3.fit([train.userId, train.movieId], train.rating, epochs=50, verbose=0)
elapsed = timeit.default_timer() - start_time


# In[155]:


y_hat = np.round(model3.predict([test.userId, test.movieId]),0)
y_true = test.rating


# In[156]:


mean_absolute_error(y_true, y_hat)


# In[157]:


#even lower error score


# In[ ]:





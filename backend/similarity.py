from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Similarity:

    #function for similairty
    def create_similarity(self, data):
        #create the count matrix as cv
        cv = CountVectorizer()
        #create the matrix based on the column comb which is the combination of them all 
        count_matrix = cv.fit_transform(data['all'].values.astype('U'))
        #create the similiaity score matrix 
        similarity = cosine_similarity(count_matrix)
        return data, similarity 

    #recommendation function-> rec
    def rec(self, m, data): #movies -> m
        m = m.lower() #make the movies lowercase 
        data, similarity = self.create_similarity(data)
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
    def convert_to_list(self, my_list):
        my_list = my_list.split(' ","') 
        #replacing the brackets []
        my_list[0] = my_list[0].replace('["', '')
        my_list[-1] = my_list[-1].replace('"]', '')
        return my_list 

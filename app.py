import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict   = pickle.load(open('movie_dict.pkl','rb'))
#Gives the list of the movies
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
 
 
 
def fetch_poster(movie_id, api_key):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US&api_key={api_key}'
 
    response = requests.get(url)
    data = response.json()

    print(data)  # Add this line to inspect the response data

    if 'poster_path' in data:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "No poster available"
   
 
 

 
 
 
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1]) [1:6]
    
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movie_list:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id, '63cdc284c98a6bd9c3f35c8f370cc856'))
       

    return recommended_movie_names,recommended_movie_posters

st.title('Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
if st.button('Recommend'):
    names,posters = recommend(selected_movie)
    
    col1,col2,col3,col4,col5 = st.columns(5)
    
    with col1:
         st.text(names[0])
         st.image(posters[0])
    
    with col2:
         st.text(names[1])
         st.image(posters[1])
    
    with col3: 
         st.text(names[2])
         st.image(posters[2])
    
    with col4: 
        st.text(names[3])
        st.image(posters[3])
    
    with col5: 
         st.text(names[4])
         st.image(posters[4])
         

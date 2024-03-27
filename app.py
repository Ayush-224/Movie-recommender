import streamlit as st
import pickle
import pandas as pd
import requests
import requests_cache

# Enable cache with expiry time
requests_cache.install_cache('tmdb_cache', expire_after=3600)  # Cache for 1 hour
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=ad1712fe98f494375e4372c9972f6330&language=en-US'.format(movie_id))
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()
    poster_path = data.get('poster_path')
    full_path="https://image.tmdb.org/t/p/w500"+poster_path
    return full_path
    
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        
        # fetch poster from tmdb API
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
        # st.text(recommended_movies_posters)
    return recommended_movies,recommended_movies_posters

movies_dict= pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity= pickle.load(open('similarity.pkl','rb'))


st.title('Movies Recommender system')
selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(posters[0])
        st.text(names[0])
    with col2:
        st.image(posters[1])
        st.text(names[1])
    with col3:
        st.image(posters[2])
        st.text(names[2])
    with col4:
        st.image(posters[3])
        st.text(names[3])
    with col5:
        st.image(posters[4])
        st.text(names[4])
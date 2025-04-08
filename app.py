import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "URL-WITH-API-KEY-HERE"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
import streamlit as st

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    st.markdown("""
        <style>
            .movie-container {
                display: flex;
                justify-content: space-evenly;
                gap: 20px; /* Ensures spacing */
                margin-top: 20px;
            }
            .movie-card {
                background: #1e1e1e;
                padding: 15px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 4px 4px 10px rgba(255, 255, 255, 0.1);
                transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out, z-index 0.3s ease-in-out;
                width: 180px;
                height: 300px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: space-between;
                position: relative; /* Needed for z-index to work */
                z-index: 1;
            }
            .movie-card:hover {
                transform: scale(1.05);
                box-shadow: 6px 6px 15px rgba(255, 255, 255, 0.2);
                z-index: 10; /* Ensures the hovered card appears above others */
            }
            .movie-title {
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                margin-top: 10px;
                text-align: center;
            }
            .movie-poster {
                width: 100%;
                height: 220px;
                border-radius: 10px;
                object-fit: cover;
                transition: opacity 0.3s ease-in-out;
            }
            .movie-poster:hover {
                opacity: 0.85;
            }
        </style>
    """, unsafe_allow_html=True)

    cols = st.columns(5, gap="large")  

    for i, col in enumerate(cols):
        with col:
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{recommended_movie_posters[i]}" class="movie-poster">
                    <p class="movie-title">{recommended_movie_names[i]}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

# import streamlit as st
# import pickle
# import pandas as pd
# import requests
#
# def fetch_poster(movie_id):
#     response = requests.get(
#         'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(
#             movie_id))
#     data = response.json()
#     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
#
#
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True,key=lambda x: x[1])[1:6]
#
#     recommended_movies = []
#     recommended_movies_posters = []
#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#
#         recommended_movies.append(movies.iloc[i[0]].title)
#         # fetch poster from API
#         recommended_movies_posters.append(fetch_poster(movie_id))
#     return recommended_movies, recommended_movies_posters
#
# movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)
#
# similarity = pickle.load(open('similarity.pkl', 'rb'))
#
# st.title('Movie Recommendation')
#
# selected_movie_name = st.selectbox(
# 'Select Movie',
# movies['title'].values)
#
# if st.button('Recommend'):
#     names,posters = recommend(selected_movie_name)
#
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         st.header(names[0])
#         st.image(posters[0])
#
#     with col2:
#         st.header(names[1])
#         st.image(posters[1])
#
#     with col3:
#         st.header(names[2])
#         st.image(posters[2])
#
#     with col4:
#         st.header(names[3])
#         st.image(posters[3])
#
#     with col5:
#         st.header(names[4])
#         st.image(posters[4])
#

# /////////////////////////////////////////////////////////////////////////////////////////////////

import streamlit as st
import pickle
import pandas as pd
import requests

# -------------------- CONFIG --------------------
TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
PLACEHOLDER_POSTER = "https://via.placeholder.com/500x750?text=No+Image"

# -------------------- POSTER FETCH FUNCTION --------------------
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
        else:
            return PLACEHOLDER_POSTER

    except requests.exceptions.RequestException:
        return PLACEHOLDER_POSTER


# -------------------- RECOMMENDATION FUNCTION --------------------
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# -------------------- LOAD DATA --------------------
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))


# -------------------- STREAMLIT UI --------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Select a Movie",
    movies["title"].values
)

if st.button("Recommend"):
    try:
        names, posters = recommend(selected_movie_name)

        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.subheader(names[i])
                st.image(posters[i], use_container_width=True)

    except Exception as e:
        st.error("⚠️ Unable to fetch recommendations. Please try again later.")

        

# ////////////////////////////////////////////////////////////////////////////////////////////////////


# import streamlit as st
# import pickle
# import pandas as pd
# import requests
# import os
#
# # -------------------- CONFIG --------------------
# TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
# FALLBACK_POSTER = "no_poster.jpg"
#
# # -------------------- POSTER FETCH --------------------
# @st.cache_data(show_spinner=False)
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
#
#     try:
#         response = requests.get(url, timeout=5)
#         response.raise_for_status()
#         data = response.json()
#
#         poster_path = data.get("poster_path")
#         if poster_path:
#             return "https://image.tmdb.org/t/p/w500/" + poster_path
#         else:
#             return FALLBACK_POSTER
#
#     except requests.exceptions.RequestException:
#         return FALLBACK_POSTER
#
#
# # -------------------- RECOMMEND FUNCTION --------------------
# def recommend(movie):
#     movie_index = movies[movies["title"] == movie].index[0]
#     distances = similarity[movie_index]
#
#     movies_list = sorted(
#         list(enumerate(distances)),
#         key=lambda x: x[1],
#         reverse=True
#     )[1:6]
#
#     recommended_movies = []
#     recommended_movies_posters = []
#
#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movies.append(movies.iloc[i[0]].title)
#         recommended_movies_posters.append(fetch_poster(movie_id))
#
#     return recommended_movies, recommended_movies_posters
#
#
# # -------------------- LOAD DATA --------------------
# movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
# movies = pd.DataFrame(movies_dict)
#
# similarity = pickle.load(open("similarity.pkl", "rb"))
#
#
# # -------------------- STREAMLIT UI --------------------
# st.set_page_config(
#     page_title="Movie Recommendation System",
#     layout="wide"
# )
#
# st.title("🎬 Movie Recommendation System")
#
# selected_movie_name = st.selectbox(
#     "Select a Movie",
#     movies["title"].values
# )
#
# if st.button("Recommend"):
#     try:
#         names, posters = recommend(selected_movie_name)
#
#         cols = st.columns(5)
#         for i in range(5):
#             with cols[i]:
#                 st.subheader(names[i])
#                 st.image(posters[i], use_container_width=True)
#
#     except Exception:
#         st.error("⚠️ Something went wrong. Please try again.")

# ///////////////////////////////////////////////////////////////////////////////////////////////

# import streamlit as st
# import pickle
# import pandas as pd
# import requests

# # -------------------- CONFIG --------------------
# TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
# FALLBACK_POSTER = "no_poster.jpg"

# # -------------------- FETCH POSTER --------------------
# @st.cache_data(show_spinner=False)
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"

#     try:
#         response = requests.get(url, timeout=5)
#         response.raise_for_status()
#         data = response.json()

#         poster_path = data.get("poster_path")
#         if poster_path:
#             return "https://image.tmdb.org/t/p/w500/" + poster_path
#         else:
#             return FALLBACK_POSTER

#     except requests.exceptions.RequestException:
#         return FALLBACK_POSTER


# # -------------------- RECOMMEND FUNCTION (FIXED) --------------------
# def recommend(movie):
#     # handle duplicate titles safely
#     matches = movies[movies["title"] == movie]

#     if matches.empty:
#         raise ValueError("Movie not found")

#     movie_index = matches.index[0]
#     distances = similarity[movie_index]

#     movies_list = sorted(
#         list(enumerate(distances)),
#         key=lambda x: x[1],
#         reverse=True
#     )[1:6]

#     recommended_movies = []
#     recommended_movies_posters = []

#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movies.append(movies.iloc[i[0]].title)
#         recommended_movies_posters.append(fetch_poster(movie_id))

#     return recommended_movies, recommended_movies_posters


# # -------------------- LOAD DATA --------------------
# movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
# movies = pd.DataFrame(movies_dict)

# similarity = pickle.load(open("similarity.pkl", "rb"))


# # -------------------- STREAMLIT UI --------------------
# st.set_page_config(
#     page_title="Movie Recommendation System",
#     layout="wide"
# )

# st.title("🎬 Movie Recommendation System")

# selected_movie_name = st.selectbox(
#     "Select a Movie",
#     movies["title"].values
# )

# if st.button("Recommend"):
#     try:
#         names, posters = recommend(selected_movie_name)

#         cols = st.columns(5)
#         for i in range(5):
#             with cols[i]:
#                 st.subheader(names[i])
#                 st.image(posters[i], use_container_width=True)

#     except Exception as e:
#         st.error("⚠️ Unable to generate recommendations for this movie.")

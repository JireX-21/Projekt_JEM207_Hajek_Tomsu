import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import geopandas as gpd
import requests
from googleapiclient.discovery import build

st.title('Netflix data project JEM207 by Hajek and Tomsu')

data = pd.read_csv('data/proccessed_data.csv')

#Graph
st.subheader('Distribution of Content Types')
content_counts = data['type'].value_counts()

fig, ax = plt.subplots()
ax.bar(content_counts.index, content_counts.values)
ax.set_xlabel('Content Type')
ax.set_ylabel('Count')
ax.set_title('Distribution of Content Types')

st.pyplot(fig)

# Graph
def filter_by_type(df, content_type):
    filtered_data = df[df['type'] == content_type]
    return filtered_data

movies = filter_by_type(data,'Movie')
tv_shows = filter_by_type(data,'TV Show')

st.subheader('Distribution of Movies and TV Shows by Release Year')

movie_counts = movies['release_year'].value_counts().sort_index()
tv_show_counts = tv_shows['release_year'].value_counts().sort_index()

fig, ax = plt.subplots()
ax.plot(movie_counts.index, movie_counts.values, label='Movies')
ax.plot(tv_show_counts.index, tv_show_counts.values, label='TV Shows')
ax.set_xlabel('Release Year')
ax.set_ylabel('Count')
ax.set_title('Distribution of Movies and TV Shows by Release Year')
ax.legend()

st.pyplot(fig)

#Graph
current_year = datetime.datetime.now().year

filtered_df = data[(data['release_year'] >= 2000) & (data['release_year'] <= current_year)]

movie_counts = filter_by_type(filtered_df,'Movie')['release_year'].value_counts().sort_index()
tv_show_counts = filter_by_type(filtered_df,'TV Show')['release_year'].value_counts().sort_index()

st.subheader('Distribution of Movies and TV Shows by Release Year (2000 - {})'.format(current_year))

fig, ax = plt.subplots()
ax.plot(movie_counts.index, movie_counts.values, label='Movies')
ax.plot(tv_show_counts.index, tv_show_counts.values, label='TV Shows')
ax.set_xlabel('Release Year')
ax.set_ylabel('Count')
ax.set_title('Distribution of Movies and TV Shows by Release Year (2000 - {})'.format(current_year))
ax.legend()

st.pyplot(fig)

#World graph

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))


merged_data = world.merge(data.groupby('continent').size().reset_index(name='movie_count'), on='continent', how='left')


st.title('Number of Movies by Continent')


fig, ax = plt.subplots(1, 1, figsize=(10, 6))
merged_data.plot(column='movie_count', cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
ax.set_title('Number of Movies by Continent')
ax.set_axis_off()


st.pyplot(fig)

#Function for visualizating frequency of different features
def most_casted_actors(data, column, top_n=10):
    data[column] = data[column].fillna('')

    actor_counts = {}

    for row in data[column]:
        for actor in row.split(','):
            actor = actor.strip()
            if actor and actor != 'Unknown':
                if actor in actor_counts:
                    actor_counts[actor] += 1
                else:
                    actor_counts[actor] = 1

    sorted_actors = sorted(actor_counts.items(), key=lambda x: x[1], reverse=True)

    top_n_actors = sorted_actors[:top_n]

    return top_n_actors

#Show/Movie finder

data['country'] = data['country'].astype(str)
data['cast'] = data['cast'].astype(str)

def filter_by_type(df, content_type):
    filtered_data = df[df['type'] == content_type]
    return filtered_data

def extract_unique_column(df, genre_column):
    unique_column = set()
    for genres in df[genre_column]:
        unique_column.update(genre.strip() for genre in genres.split(','))
    return unique_column

unique_countries = extract_unique_column(data,'country')
unique_countries_list = sorted(list(unique_countries))

movie_data = filter_by_type(data,'Movie')
unique_genres = extract_unique_column(movie_data,'genre')
unique_movie_list = list(unique_genres)

movie_data = filter_by_type(data,'TV Show')
unique_genres = extract_unique_column(movie_data,'genre')
unique_show_list = list(unique_genres)

st.title('Movie recommender')

type = st.radio('Select type: ', ('TV Show', 'Movie'))

countries = st.multiselect('Countries: ', unique_countries_list)

year_interval = st.multiselect('Year interval: ',
                         ['1971-1980', '1981-1990', '1991-2000','2001-2010','2011-2020','2021-2030'])

if (type == 'Movie'):
    genre = st.multiselect('Genre: ', unique_movie_list)
else:
   genre = st.multiselect('Genre: ', unique_show_list)


filtered_films = data[
    (data['type'] == type) &
    (data['year_interval'].isin(year_interval))&
    (data['genre'].isin(genre))
]

filtered_films = filtered_films[
    filtered_films['country'].apply(lambda countries_list: any(country in countries for country in countries_list.split(', ')))
]

if not filtered_films.empty:
    st.table(filtered_films[['title', 'release_year', 'country', 'genre']])
else:
    st.write('No films match the selected criteria.')

#API trailer

YOUTUBE_API_KEY = ''

def search_movie_trailer(movie_title):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(
        q=f'{movie_title} trailer',
        type='video',
        part='id',
        maxResults=1
    ).execute()

    if 'items' in search_response:
        video_id = search_response['items'][0]['id']['videoId']
        return f'https://www.youtube.com/watch?v={video_id}'
    else:
        return None

st.title('Film Trailer')

movie_title = st.text_input('Enter Movie Title:')
if st.button('Search Trailer'):
    trailer_url = search_movie_trailer(movie_title)
    if trailer_url:
        st.video(trailer_url)
    else:
        st.write('Trailer not found.')

#TOP actors
st.title('Top Actors on Netflix')

data_2 = most_casted_actors(data, 'cast')
genres, counts = zip(*data_2)

plt.figure(figsize=(10, 6))
plt.barh(genres, counts, color='#007cb9')
plt.xlabel('Count')
plt.title('Top Actors on Netflix')
plt.gca().invert_yaxis()
plt.tight_layout()

st.pyplot(plt)

#TOP genres
st.title('Top Genres on Netflix')

selected_type = st.selectbox('Select Type', ['All', 'Movie', 'TV Show'])

if selected_type == 'Movie':
    filtered_data = data[data['type'] == 'Movie']
elif selected_type == 'TV Show':
    filtered_data = data[data['type'] == 'TV Show']
else:
    filtered_data = data

data = most_casted_actors(filtered_data, 'genre')
genres, counts = zip(*data)

plt.figure(figsize=(10, 6))
plt.barh(genres, counts, color='#007cb9')
plt.xlabel('Count')
plt.title('Top Genres on Netflix')
plt.gca().invert_yaxis()
plt.tight_layout()

st.pyplot(plt)
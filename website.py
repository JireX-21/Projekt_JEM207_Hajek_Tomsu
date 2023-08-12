import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import geopandas as gpd

st.title("Netflix data project JEM207 by Hajek and Tomsu")

data = pd.read_csv("proccessed_data.csv")

#Graph
st.subheader("Distribution of Content Types")
content_counts = data['type'].value_counts()

fig, ax = plt.subplots()
ax.bar(content_counts.index, content_counts.values)
ax.set_xlabel('Content Type')
ax.set_ylabel('Count')
ax.set_title('Distribution of Content Types')

st.pyplot(fig)

# Graph
movies = data[data['type'] == 'Movie']
tv_shows = data[data['type'] == 'TV Show']

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

movie_counts = filtered_df[filtered_df['type'] == 'Movie']['release_year'].value_counts().sort_index()
tv_show_counts = filtered_df[filtered_df['type'] == 'TV Show']['release_year'].value_counts().sort_index()

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

#Show/Movie finder

type = st.radio("Select type: ", ('TV Show', 'Movie'))

countries = st.multiselect("Countries: ",
                     ['Afghanistan', 'Albania', 'Algeria', 'Angola', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bangladesh', 'Belarus', 'Belgium', 'Bermuda', 'Botswana', 'Brazil', 'Bulgaria', 'Burkina Faso', 'Cambodia', 'Cameroon', 'Canada', 'Cayman Islands', 'Chile', 'China', 'Colombia', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Dominican Republic', 'East Germany', 'Ecuador', 'Egypt', 'Ethiopia', 'Finland', 'France', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Guatemala', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Latvia', 'Lebanon', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malawi', 'Malaysia', 'Malta', 'Mauritius', 'Mexico', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Nigeria', 'Norway', 'Pakistan', 'Palestine', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Russia', 'Samoa', 'Saudi Arabia', 'Senegal', 'Serbia', 'Singapore', 'Slovakia', 'Slovenia', 'Somalia', 'South Africa', 'South Korea', 'Soviet Union', 'Spain', 'Sri Lanka', 'Sudan', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Thailand', 'Turkey', 'Uganda', 'Uknown', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Vatican City', 'Venezuela', 'Vietnam', 'West Germany', 'Zimbabwe'])

year_interval = st.multiselect("Year interval: ",
                         ['1971-1980', '1981-1990', '1991-2000','2001-2010','2011-2020','2021-2030'])

if (type == "Movie"):
    genre = st.multiselect("Genre: ", 
                         ['Classic Movies', 'Action & Adventure', 'Documentaries', 'Comedies', 'Stand-Up Comedy', 'Faith & Spirituality', 'Horror Movies', 'Anime Features', 'Cult Movies', 'Dramas', 'Music & Musicals', 'LGBTQ Movies', 'Thrillers', 'Children & Family Movies', 'International Movies', 'Sports Movies', 'Romantic Movies', 'Sci-Fi & Fantasy', 'Movies', 'Independent Movies'])
else:
   genre = st.multiselect("Genre: ", 
                         ['Classic & Cult TV', 'TV Mysteries', 'Docuseries', "Kids' TV", 'Crime TV Shows', 'Teen TV Shows', 'Romantic TV Shows', 'Science & Nature TV', 'TV Dramas', 'Reality TV', 'TV Action & Adventure', 'TV Shows', 'Korean TV Shows', 'Anime Series', 'TV Thrillers', 'Stand-Up Comedy & Talk Shows', 'TV Sci-Fi & Fantasy', 'TV Comedies', 'Spanish-Language TV Shows', 'International TV Shows', 'TV Horror', 'British TV Shows']) 


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
    st.write("No films match the selected criteria.")


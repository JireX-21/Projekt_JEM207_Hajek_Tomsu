# Project_Hajek_Tomsu
This is a repository for our Data Processing in Python project. Collaborative work of Jiří Hájek and Vojtěch Tomšů.
# Netflix cinematographics database analysis + movie recommendation application

First part of our code is dedicated to work with data, cleaning and inspecting it. Then, we proceed in deeper analysis and visualization and third part of our work is program, that recommends user a movie based on the inputs given by the user. After a movie is recommended, user can watch trailer of it directly on our streamlit website, without the need of leaving it, as we use API request to import the trailer from Youtube. 

We obtained our dataset from https://www.kaggle.com/datasets/ariyoomotade/netflix-data-cleaning-analysis-and-visualization?datasetId=2437124&sortBy=voteCount - here is brief introduction to it: 
    Netflix is a popular streaming service that offers a vast catalog of movies, TV shows, and original contents. This dataset is a cleaned version of the original version which can be found here. The data consist of contents added to Netflix from 2008 to 2021. The oldest content is as old as 1925 and the newest as 2021.

# Obtaining API key
For the trailer you will have obtain your own API key via https://console.cloud.google.com, where you will create a project a than in the sidebar click on credentials. On the credentials side you will click the "Create credentials" button and select "API key.". You will have create your own ".env" file on your device and insert API_KEY= 'your_API_key'.

## Project structure


```
│ main.ipynb                      # main script
│ website.py                      # final application with data visualization and movie recommender; final product
│ README.md                       # guide to our project code and structure
│ requirements.txt                # requirements
│
└───data                              
    ├───netflix_titles.csv        # raw dataset
    ├───proccessed_data.csv       # final dataset
```

## Arguments

* "type"
    * This argument lets you pick Movie or TV Show

* "countries"
    * Argument lets you choose desired country of cinematographic origin

* "year interval"
    * Argument for picking a decade in which was the movie made
    * We decided to split years in decades, as it provides more user-friendly solution

* "genre"
    * Argument that offers various kinds of genres of either TV Shows and Movies
    * The offer of genres differ based on user's choice in "type" argument


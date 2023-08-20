# Project_Hajek_Tomsu
This is a repository for our Data Processing in Python project. Collaborative work of Jiří Hájek and Vojtěch Tomšů.
# Netflix cinematographics database analysis + movie recommendation application

First part of our code is dedicated to work with data, cleaning and inspecting it. Then, we proceed in deeper analysis and visualization and third part of our work is program, that recommends user a movie based on the inputs given by the user.

We obtained our dataset from https://www.kaggle.com/datasets/ariyoomotade/netflix-data-cleaning-analysis-and-visualization?datasetId=2437124&sortBy=voteCount - here is brief introduction to it: 
    Netflix is a popular streaming service that offers a vast catalog of movies, TV shows, and original contents. This dataset is a cleaned version of the original version which can be found here. The data consist of contents added to Netflix from 2008 to 2021. The oldest content is as old as 1925 and the newest as 2021.

## Project structure


```
│ main.py                             # main script
│ website.py                          # final application with data visualization and movie recommender; final product
│ README.md                           # guide to our project code and structure
│
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


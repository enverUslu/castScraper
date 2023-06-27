## Main Project ##
#castScraper by Enver Uslu [6-27-2023]
#I made this project for my programming portfolio,
#educational use and practice for web scraping only.
#github.com/enverUslu

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

import requests
from imdb import IMDb

# Creating an IMDb object
ia = IMDb()

# Asking the user for a movie name
filmName = input("Enter a movie name: ")

# Searching for movies using the given name
movies = ia.search_movie(filmName)

# Checking if any movies are found - hoping they are.
if len(movies) > 0:
    # Get the first movie from the search results
    movie = movies[0]

    # Get the IMDb ID of the movie
    imdb_id = movie.getID()

    # Construct the IMDb URL using the IMDb ID
    url = f"https://www.imdb.com/title/tt{imdb_id}/fullcredits"

    # Print the URL
    print("URL:", url)
else:
    print("No movies found.")
    
if movie is not None:
    # Get the title of the movie
    title = movie.get('title')

    # Display the movie's name
    print("Movie Title:", title)
    print("----------")
else:
    print("Movie not found.")
    print("----------")



print("--CAST--")
# URL of the page to scrape

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object with the response text
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the table rows containing actor information
actor_rows = soup.select('tr.odd, tr.even')

# Loop through the actor rows and extract the actor names and roles
for row in actor_rows:
    # Extract actor name
    actor_name_element = row.select_one('td.primary_photo a img')
    actor_name = actor_name_element.get('alt') if actor_name_element else "N/A"

    # Extract actor role
    actor_role_element = row.select_one('td.character a')
    actor_role = actor_role_element.text.strip() if actor_role_element else "N/A"

    if actor_name != "N/A" and actor_role != "N/A":
        print(f"Actor: {actor_name}")
        print(f"Role: {actor_role}")
        print("----------")

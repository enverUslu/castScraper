#castScraper by Enver Uslu [6-27-2023] - SearchLog ver.
#I made this project for my programming portfolio,
#educational use and practice for web scraping only.
#github.com/enverUslu

#This version of castScraper saves every search and their result into
#a log file called 'searchedMovies.log'.

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests
from imdb import IMDb
import sys

# Define the path to the log file
log_file_path = "searchedMovies.log"

# Create a file object to write the log
log_file = open(log_file_path, 'a')

# Create a function to redirect the output to both the console and the log file
def redirect_output_to_file(file_object):
    # Create a class that writes to multiple file objects
    class MultiFile(object):
        def __init__(self, *files):
            self.files = files

        def write(self, text):
            for file in self.files:
                file.write(text)

        def flush(self):
            for file in self.files:
                file.flush()

    # Redirect the output to the console and the log file
    sys.stdout = MultiFile(sys.stdout, file_object)

# Redirect the output to the console and the log file
redirect_output_to_file(log_file)

# Creating an IMDb object
ia = IMDb()

# Define a function to prompt for a movie name
def prompt_movie_name():
    print("Enter a movie name: ")
    sys.stdout.flush()  # Flush the stdout buffer
    return input()

# Prompt the user for a movie name
filmName = prompt_movie_name()

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
    print('##################################################')
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
        output = f"Actor: {actor_name}\nRole: {actor_role}\n----------"
        print(output)

# Close the log file
log_file.close()

# Restore the standard output
sys.stdout = sys.__stdout__

# Deleting the first line from the searchedMovies.log
# because it contains 'Enter a movie name: '
def remove_text_from_log_file(file_path, text_to_remove):
    # Open the .log file in read mode
    with open(file_path, 'r') as file:
        # Read the contents
        contents = file.read()

    # Replace the specific text with an empty string
    modified_contents = contents.replace(text_to_remove, '')

    # Open the .log file in write mode
    with open(file_path, 'w') as file:
        # Write the modified contents back into the .log file
        file.write(modified_contents)

    print("Specific text removed from the .log file.")


# Provide the path to your .log file
log_file_path = 'searchedMovies.log'

# Provide the specific text you want to remove
text_to_remove = 'Enter a movie name: '

# Call the function to remove the specific text from the .log file
remove_text_from_log_file(log_file_path, text_to_remove)

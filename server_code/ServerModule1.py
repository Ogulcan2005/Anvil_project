import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def update_movie(movie, movie_data):
    if movie_data['director'] and movie_data['movie_name'] and movie_data['summary'] and movie_data['year']:
        movie.update(**movie_data)

@anvil.server.callable
def add_movie(movie_data):
    if movie_data['director'] and movie_data['movie_name'] and movie_data['summary'] and movie_data['year']:
        app_tables.movies.add_row(**movie_data)

@anvil.server.callable
def delete_movie(movie):
    movie.delete()

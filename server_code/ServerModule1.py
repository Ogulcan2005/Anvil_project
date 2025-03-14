import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import base64
from cloudant.client import Cloudant

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

@anvil.server.callable
def decode(enc, key):
    dec = []
    enc2 = base64.urlsafe_b64decode(enc)
  
    for i in range(len(enc2)):

        key_c = key[i % len(key)]

        dec_c = chr((256 + enc2[i] - ord(key_c)) % 256)

        dec.append(dec_c)

    decB64 = "".join(dec)

    return decB64

 

 

@anvil.server.callable

def get_userprofiles():
  licfile = anvil.secrets.get_secret('licfile')
  lickey = anvil.secrets.get_secret('lickey')
  deckey = anvil.secrets.get_secret(('deckey'))
  declicense = decode(licfile, lickey)
  licwords = str(declicense).split('[---]')
  sgaccount = licwords[7]
  dbconfigkey = licwords[17]
  dbconfigpwd = licwords[26]
  client = Cloudant(dbconfigkey, dbconfigpwd, account=sgaccount)
  client.connect()
  my_db = client['userprofiles']
  docs_found = my_db.all_docs(include_docs=True)
  dataregels = docs_found['rows']
  numlen = len(dataregels)
  for index in range (0, numlen):
    if 'doc' in dataregels[index]:
      user_data = (dataregels[index]['doc'])
      if 'FIRSTNAME' in user_data:
        enc_firstname = (user_data['FIRSTNAME'])
        enc_surname = (user_data['SURNAME'])
        enc_email = (user_data['EMAIL'])
        firstname = decode(enc_firstname, deckey)
        surname = decode(enc_surname, deckey)
        email = decode(enc_email, deckey)
        add_info(firstname, surname, email)
        #print(f"Voornaam: {firstname} - Achternaam: {surname} - Email: {email}")
        

  return docs_found['rows']

def add_info(fn, sn ,em):
  app_tables.movies.add_row(movie_name=fn, director=sn)
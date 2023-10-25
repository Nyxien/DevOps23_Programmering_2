from urllib import request as urlrequest
import json, ssl
from flask import Flask, render_template, jsonify
from datetime import *

# Här skapas en Flask-applikation med namnet av den den nuvarande modulen.
app = Flask(__name__)

def get_prices(year, month, day, price_range):
    '''Här skapas en funktion get_prices som tar in våra parametrarna year, month, day och price_range. 
    Denna funktion anropar en extern API som hämtar data om elpriserna vid en viss tidpunkt och sedan returnerar den.'''
    url = f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{price_range}.json"
    try: # Här försöker koden hämta data från den specificerade URL:en.
        response = urlrequest.urlopen(url)
        data = json.loads(response.read()) # Här konverteras den hämtade datan till JSON-format. I detta fall så är datan vi hämtar redan i json men det det kan vara bra ifall det någon gång skulle ändras och det är mer konsekvent.
        return data
    except urlrequest.HTTPError as e:
        if e.code == 404:
            return {"error": "404 - Not found"}

@app.route("/", methods=['GET', 'POST'])
def index():
    if urlrequest.method == 'POST':

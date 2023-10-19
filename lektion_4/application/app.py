from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    '''Plats för kommentarer'''

    #Här placeras koden



    return render_template('index.html')
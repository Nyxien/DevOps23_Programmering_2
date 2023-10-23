from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    '''Plats för kommentarer'''

    #Här placeras koden



    return render_template('index.html')

@app.route("/form")
def form():
    '''plats för kommentarer'''

    #koden skrivs här

    return render_template('form.html')

@app.route("/api", methods=["post"])
def index():
    '''Plats för kommentarer'''

    #Här placeras koden



    return render_template('index.html', data=data)
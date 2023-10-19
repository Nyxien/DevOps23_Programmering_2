from flask import render_template, Flask
import pandas as pd


app = Flask(__name__)
dictionary = {
    "landsdel" : ["Götaland", "Götaland", "Götaland", "Svealand", "Svealand", "Norrland", "Norrland", "Norrland", "Norrland", "Norrland"],
    "landskap" : ["Östergötland", "Östergötland", "Västergätland", "Södermanland", "Södermanland", "Norrbotten", "Gästrikland", "Ångermanland", "Ångermanland", "Ångermanland"],
    "Stad" : ["Linköping", "Motala", "Mjölby", "Mariefred", "Nyköping", "Piteå", "Sandviken", "Sollefteå", "Kramfors", "Örnsköldsvik"]
}
df = pd.DataFrame(dictionary)
html = df.to_html(classes="table")


@app.route("/")
def index():
    return render_template("template.htm", data=html)


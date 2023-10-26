from urllib import request as urlrequest, parse
import json, ssl
from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
from func import url_to_dataframe as df

# Here, create a Flask application with the current module's name.
app = Flask(__name__)

def get_prices(year, month, day, price_range):
    try:
        input_date = datetime(int(year), int(month), int(day))
        min_date = datetime(2022, 11, 1)
        max_date = datetime.now() + timedelta(days=1)

        if input_date < min_date or input_date > max_date:
            return False

        url = f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{price_range}.json"
        context = ssl._create_unverified_context()
        response = urlrequest.urlopen(url, context=context)
        data = json.loads(response.read())
        return data

    except urlrequest.HTTPError as e:
        if e.code == 404:
            return {"error": "404 - Not found"}
        else:
            return {"error": "An HTTP error occurred"}

    except ValueError:
        return {"error": "Invalid input data"}

    except Exception as e:
        return {"error": f"An error occurred: {e}"}

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve the input values.
        year = request.form['year']
        month = request.form['month']
        day = request.form['day']
        price_range = request.form['price_range']

        data = get_prices(year, month, day, price_range)

        if data:
            if "error" in data:
                return render_template('index.html', error=data["error"])
            else:
                return render_template('index.html', data=data, table=df.to_html())
        else:
            return render_template('index.html', error="Invalid date range.")

    return render_template('index.html')

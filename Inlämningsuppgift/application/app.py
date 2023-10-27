from urllib import request as urlrequest, parse
import json, ssl
from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta


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
        
    
        # Här konverterar vi time_Start och time_end till tid stampar så det är mer läsbart för användaren. Detta görs genom att matcha tidsformatet i våran api och omvandla den.
        for item in data:
            item['time_start'] = datetime.strptime(item['time_start'], "%Y-%m-%dT%H:%M:%S%z").strftime("%H:%M")
            item['time_end'] = datetime.strptime(item['time_end'], "%Y-%m-%dT%H:%M:%S%z").strftime("%H:%M")

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
        # Hämtar input values
        year = request.form['year']
        month = request.form['month']
        day = request.form['day']
        price_range = request.form['price_range']

        data = get_prices(year, month, day, price_range)

        if data:
            if "error" in data:
                return render_template('index.html', error=data["error"])
            else:
                return render_template('index.html', data=data)
        else:
            return render_template('index.html', error="Invalid date range.")
    return render_template('index.html')
from urllib import request as urlrequest
import json, ssl
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta


app = Flask(__name__) # Här skapas en instans av Flask applikationen

def get_prices(year, month, day, price_range): 
    try: # Här anger vi intervallet av den tillåtna indatan.
        input_date = datetime(int(year), int(month), int(day))
        min_date = datetime(2022, 11, 1)
        max_date = datetime.now() + timedelta(days=1)

        # Kontrollerar om inputdatan är inom det tillåtna intervallet
        if input_date < min_date or input_date > max_date:
            return False
        
        formatted_month = str(month).zfill(2) # Här försäkrar vi att datan som matas in blir i två siffror, t.ex januari är "01" istället för "1". Detta är för att månaderna/dagarna ska formateras rätt till våran API.
        formatted_day = str(day).zfill(2) # Som ovan formateras dagen till två siffror då.

        # Skapar URL för att hämta data från api som en f sträng för att kunna sätta in datan.
        url = f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{formatted_month}-{formatted_day}_{price_range}.json"
        context = ssl._create_unverified_context() # Här skapar vi en osäker SSL uppkoppling, detta bör endast användas i en testmiljö och inte i produktion. Fördelarna med är enklare testning, förenklad felsökning då man kan fokusera på själva funktionaliteten i applikationen och undvika att blockeras av SSL relaterade problem.
        response = urlrequest.urlopen(url, context=context)
        data = json.loads(response.read())
        
    
        # Här konverterar vi time_Start och time_end till tid stampar så det är mer läsbart för användaren. Detta görs genom att matcha tidsformatet i våran api och omvandla den.
        for item in data:
            item['time_start'] = datetime.strptime(item['time_start'], "%Y-%m-%dT%H:%M:%S%z").strftime("%H:%M")
            item['time_end'] = datetime.strptime(item['time_end'], "%Y-%m-%dT%H:%M:%S%z").strftime("%H:%M")

        return data
    
    except urlrequest.HTTPError as e: # Hanterar HTTP fel
        if e.code == 404:
            return {"error": "404 - Not found"}
        else:
            return {"error": f"An HTTP error occurred: {e}"}

    except ValueError: # Hanterar ogiltig input
        return {"error": "Invalid input data"}

    except Exception as e: # Här hanteras alla andra typer av fel
        return {"error": f"An error occurred: {e}"}

@app.route("/", methods=['GET', 'POST'])
def index(): # Endpoint för formuläret

    # Hämtar det nuvarande året
    current_year = datetime.now().year

    if request.method == 'POST':
        # Hämtar input values från formuläret
        year = request.form['year']
        month = request.form['month']
        day = request.form['day']
        price_range = request.form['price_range']

        data = get_prices(year, month, day, price_range)

        return redirect(url_for('result', year=year, month=month, day=day, price_range=price_range))
    return render_template('index.html', current_year=current_year)



@app.route('/result', methods=['GET', 'POST'])
def result(): # Endpoint för resultatet efter användaren har fyllt in formuläret.

    if request.method == 'POST':
        # Hämtar input värden från formuläret och anropar get_prices funktionen
        year = request.form['year']
        month = request.form['month']
        day = request.form['day']
        price_range = request.form['price_range']

        data = get_prices(year, month, day, price_range)

        # Hanterar olika fall, såsom felmeddelanden och ogiltliga datum.
        if data:
            if "error" in data:
                return render_template('result.html', error=data["error"])
            else:
                return render_template('result.html', data=data)
        else:
            return render_template('result.html', error="Invalid date range.")

    return render_template('result.html')

@app.errorhandler(404)
def page_not_found(e): # Här skapar vi en endpoint som hanterar 404 kod och tar en till en anpassad sida.
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
from urllib import request as urlrequest
import pytest
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from application.app import app, get_prices #Här hämtar vi get_prices funktionen från våran app.py samt våran app.py för att testa

def test_Is_online_index():
    '''Här görs en request.get fär att kolla om våran endpoint är funktionell'''
    try:
        response = urlrequest.urlopen("http://127.0.0.1:5000", timeout=10)
        assert response.getcode() == 200
    except Exception as e:
        pytest.fail(f"Request failed with error: {e}")

def test_url_running():
    '''Skapar ett test case som simulera en flask request utan att behöva starta servern'''
    with app.test_client() as client:
        try:
            response = client.get('/')
            assert response.status_code == 200
        except ConnectionError:
            pytest.fail("Failed to start")

def test_Is_API_online_index():
    '''Här testar vi om våran API är tillgänglig'''
    url = "https://www.elprisetjustnu.se/api/v1/prices/2023/11-04_SE3.json"
    try:
        response = urlrequest.urlopen(url, )
        assert response.getcode() == 200
    except Exception as e:
        pytest.fail(f"Request failed with error: {e}")


def test_get_prices():
    '''Denna test_case testar våran funktion get_prices med olika typer av data för att säkerställa att koden hanterar giltig och ogiltig input'''
    # Testa giltig input
    valid_year = 2023 # giltig år   
    valid_month = 11 # giltig månad
    valid_day = 3 #giltig dag
    valid_price_range = 'SE1'
    data = get_prices(valid_year, valid_month, valid_day, valid_price_range)
    assert data is not False

    # Testa ogiltig input
    invalid_year = 2025 # ogiltig år
    invalid_month = 13  # Ogiltig månad
    invalid_day = 32  # Ogiltig dag
    invalid_price_range = 'invalid_range'
    data = get_prices(invalid_year, invalid_month, invalid_day, invalid_price_range)
    assert data == {"error": "Invalid input data"}

    # Testa datumintervallfel
    date_interval_year = 2021
    date_interval_month = 10
    date_interval_day = 20
    date_interval_price_range = 'interval_range'
    data = get_prices(date_interval_year, date_interval_month, date_interval_day, date_interval_price_range)
    assert data == False

def test_404_error_handling():
    '''I denna test case simulerar vi ett 404 scenario i våran flask app för att testa om vår felkod returneras'''
    with app.test_request_context():
        # Simulera ett scenario där API-anropet returnerar en 404-felkod
        with pytest.raises(Exception) as e_info:
            get_prices("2023", "13", "32", "SE3")  # Ange ett ogiltigt datum för att utlösa en 404-felkod
            assert "404" in str(e_info.value)  # Kontrollera om felmeddelandet innehåller "404"
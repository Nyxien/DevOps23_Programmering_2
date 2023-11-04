from urllib import request as urlrequest
from flask import Flask
import pytest
from requests.exceptions import ConnectionError
import ssl
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
    giltigt_ar = 2023
    giltig_manad = 11
    giltig_dag = 3
    giltigt_prisintervall = 'nagot_intervall'
    data = get_prices(giltigt_ar, giltig_manad, giltig_dag, giltigt_prisintervall)
    assert data is not False

    # Testa ogiltig input
    ogiltigt_ar = 2025
    ogiltig_manad = 13  # Ogiltig månad
    ogiltig_dag = 32  # Ogiltig dag
    ogiltigt_prisintervall = 'nagot_ogiltigt_intervall'
    data = get_prices(ogiltigt_ar, ogiltig_manad, ogiltig_dag, ogiltigt_prisintervall)
    assert data == {"error": "Invalid input data"}

    # Testa datumintervallfel
    datumintervall_fel_ar = 2021
    datumintervall_fel_manad = 10
    datumintervall_fel_dag = 20
    datumintervall_fel_prisintervall = 'något_intervall'
    data = get_prices(datumintervall_fel_ar, datumintervall_fel_manad, datumintervall_fel_dag, datumintervall_fel_prisintervall)
    assert data == False


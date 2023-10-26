import pytest
import flask
import ssl
from urllib import request, response
#from flask import Flask
from application import app, func

context = ssl._create_unverified_context()



def test_Has_endpoint_log():
    """
    GIVEN server is running
    WHEN a user tries to access log
    THEN the server responds
    """
    context = ssl._create_unverified_context()

    with pytest.raises(request.HTTPError):
        request.urlopen("http://127.0.0.1:5000/api", context=context, timeout=10)



# # Den här uppgiften går ut på att skapa lite mer funktionalitet i vår app


########
# Uppdatera countrycode i form.html till en <select> med tillgängliga alternativ från externt API, istället för en <input> med fritext.
#
# 1. <select> från Bootstrap: https://getbootstrap.com/docs/5.3/forms/select/
#
# 2. Möjliga alternativ fiiner du här: https://date.nager.at/swagger/index.html
#    Endpoint: Available countries
#    Gör om svaret från API:et från json till en lista av dictionaries och
#    spara resultatet i en variabel: countries = json.loads(resultatet)
#
# 3. Skicka countries till templaten med render_template, och lägg till alternativen i <select> med en jinja for-loop.
#    Jinja docs: https://jinja.palletsprojects.com/en/3.1.x/templates/#for
#    Ex: <option value="se">Sweden</option>

def test_Form_has_select():
    with request.urlopen("http://127.0.0.1:5000/form", context=context, timeout=10) as response:
        html = str(response.read())
        assert "</select>" in html

def test_Form_has_select_options():
    with request.urlopen("http://127.0.0.1:5000/form", context=context, timeout=10) as response:
        html = str(response.read())
        assert '<option value="SE">Sweden</option>' in html

########
# Hämta en tabell med helgdagar redan när du kommer till /index baserat på besökarens country code, och nuvarande årtal.
#
# 1. Hämta din offentliga IP adress, samt countrycode genom ett anrop till CloudFlare's API https://1.1.1.1/cdn-cgi/trace
#    Använd python för att bryta ut informationen ur resultatet och spara ner dessa värden i variabler.
#    Tips: str.split(), for loops
#
# 2. När någon kommer till endpoint '/', använd samma funktionalitet som i din endpoint "/api" för att hämta en tabell baserat på deras country_code
#    och dagens årtal. Gör ett anrop till https://date.nager.at/swagger/index.html för att få helgdagarna som json att senare lägga till i {{data}}.

def test_Endpoint_index_country_lookup():
    with request.urlopen("http://127.0.0.1:5000", context=context, timeout=10) as response:
        html = str(response.read())
        assert "Sweden" in html

########
# 1. Ändra rubriken i H1 på dina sidor till en variabel med namn <h1>{{headline}}</h1> och skicka en unik rubrik per endpoint via render_template() (dvs. jinja)
#
# /         "Welcome!"
# /form     "Please fill in the form."
# /api      "Thanks for using our service!"

def test_Endpoint_index_title():
    with request.urlopen("http://127.0.0.1:5000", context=context, timeout=10) as response:
        html = str(response.read())
        assert "Welcome!" in html

def test_Endpoint_form_title():
    with request.urlopen("http://127.0.0.1:5000/form", context=context, timeout=10) as response:
        html = str(response.read())
        assert "Please fill in the form." in html

#def test_Endpoint_api_title():
#    with request.urlopen("http://127.0.0.1:5000/api", context=context, timeout=10) as response:
#        html = str(response.read())
#        assert "Thanks for using our service!" in html


########
# 1. Skapa en meddelande-yta på index.html med en {{message}} variabel


########
# 1. Fånga upp 404 
# 2. Skicka vidare till /index. Tips ändringen sker i app.py 
# 3. Skicka med ett meddelande till {{message}} i render_template

def test_catch_404():
    with request.urlopen("http://127.0.0.1:5000/log", context=context, timeout=10) as response:
        html = str(response.read())
        assert "404" not in html


########
# 1. Fånga upp 405 från när man skickar data till /api med GET (URL i browsern). Tips ändringen sker i app.py 
# 2. Skicka vidare till /index 
# 3. Skicka med ett meddelande till {{message}} i render_template

def test_catch_405():
    with request.urlopen("http://127.0.0.1:5000/api", context=context, timeout=10) as response:
        html = str(response.read())
        assert "Method Not Allowed" not in html


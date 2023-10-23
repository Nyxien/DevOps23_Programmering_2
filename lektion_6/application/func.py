# Den här filen innehåller funktionalitet som inte är specific för Flask och servern.
# Eftersom flask inte har funktioner för att ropa på andra servrar, använder vi i denna modul istället urllib.
# Vi har nedan importerat request från urllib för att kunna ropa på externa API:er.

from urllib import request

# SSL står för Secure Socket Layer och handlar om krypterade kopplingar mellan klient och server, t.ex via HTTPS, eller SSH
import ssl

# Denna innehåller funktioner för att ladda (load, loads) och skapa (dump, dumps) JSON från python-variabler
import json

# Vi använder pandas för att arbeta med data i tabell-form. 
# Ett mycket kraftfullt ramverk för data-manipulation som vi bara skrapar på ytan av i denna kurs.
import pandas as pd


def json_url_to_html_table(data_url, columns=None):
    '''Denna funktion tar en URL, går till den platsen och hämtar resultatet
        Funktionen förväntar sig JSON som sedan laddas in i ett Pandas DataFrame (tabell) som översätts till en HTML-tabell.'''

    # Här skapar vi en regel som säger att vi accepterar att uppkopplingen mot API:et inte är krypterat
    context = ssl._create_unverified_context()

    # Till skillnad från i lektion_4 har vi nu lagt in den kod vi inte har full kontroll över i en try statement.
    # Detta för att vi inte kan vara säkra på att sidan som URL pekar till kommer att svara, eller ens att nätverket är tillgängligt
    try:
        # Läs informationen som returneras från addressen (URL)
        json_data = request.urlopen(data_url, context=context).read()
        # Gör om json (vilken kommer som en binär sträng) till en dictionary som är fullt läsbar med Python
        data = json.loads(json_data)

        # Skapa en Pandas DataFrame med innehållet i vår dictionary.
        # Om vi skickade med en lista med kolumnnamn så returnera endast dem som en HTML-tabell, annars tar vi med alla existerande kolumner
        df = pd.DataFrame(data)
        if columns==None:
            table_data = df.to_html(classes="table p-5", justify="left")    
        else:
            table_data = df.to_html(columns=columns,classes="table p-5", justify="left")

        # Returnera HTML-tabellen till app.py där ifrån funktionen ropades på
        return table_data

    # Fånga alla eventuella Exception som kan uppstå, t.ex HTTPException från request och returnera det istället för en html-tabell till anropet
    # Här skulle man kunna hantera specifika Exception, men för nu så plockar vi dem alla.
    except Exception as err:
        return err



# Samma funktion som ovan (json_url_to_html_table) men för XML-data
def xml_url_to_html_table(data_url, xpath="", columns=None):
    '''Denna funktion tar en URL, går till den platsen och hämtar resultatet
        Funktionen förväntar sig ett XML-format (t.ex RSS) som sedan laddas in i ett Pandas DataFrame (tabell) som översätts till en HTML-tabell.'''

    # Här skapar vi en regel som säger att vi accepterar att uppkopplingen mot API:et inte är krypterat
    context = ssl._create_unverified_context()

    # Till skillnad från i lektion_4 har vi nu lagt in den kod vi inte har full kontroll över i en try statement.
    # Detta för att vi inte kan vara säkra på att sidan som URL pekar till kommer att svara, eller ens att nätverket är tillgängligt
    try:
        # Läs informationen som returneras från addressen (URL)
        xml = request.urlopen(data_url, context=context).read()

        # Skapa en DataFrame direkt från XML med funktionen read_xml() i Pandas.
        # Om vi skickade med en lista med kolumnnamn så returnera endast dem som en HTML-tabell, annars tar vi med alla existerande kolumner
        df = pd.read_xml(xml, xpath=xpath)
        if columns==None:
            table_data = df.to_html(classes="table p-5", justify="left")    
        else:
            table_data = df.to_html(columns=columns,classes="table p-5", justify="left")

        # Returnera HTML-tabellen till app.py där ifrån funktionen ropades på
        return table_data

    # Fånga alla eventuella Exception som kan uppstå, t.ex HTTPException från request och returnera det istället för en html-tabell till anropet
    # Här skulle man kunna hantera specifika Exception, men för nu så plockar vi dem alla.
    except Exception as e:
        return e

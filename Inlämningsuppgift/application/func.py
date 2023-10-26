import json
from urllib import request
import pandas as pd

def url_to_dataframe(data_url):
    try:
        response = request.urlopen(data_url)
        data = response.read().decode('utf-8')
        data = json.loads(data)

        df = pd.DataFrame(data)
        df['time_start'] = pd.to_datetime(df["time_start"])
        df['year'] = df["time_start"].dt.year
        df['month'] = df["time_start"].dt.month
        df['day'] = df["time_start"].dt.day

        return df
    except request.HTTPError as e:
        if e.code == 404:
            return {"error": "404 - Not found"}
        else:
            return {"error": f"{e.code} - {e.reason}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
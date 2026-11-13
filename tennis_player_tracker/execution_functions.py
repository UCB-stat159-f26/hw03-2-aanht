import requests
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def _fetch_js(name):
    """
	Downloads JavaScript data and ensures player names are valid.
	"""
    url = f"https://www.tennisabstract.com/jsmatches/{name}Career.js"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    
    # error message if invalid
    if response.status_code == 404 or "var morematchmx" not in response.text:
        raise ValueError(f"Player '{name}' not found.")
    return response.text

def _parse_js(js_text):
    """Strips JavaScript variables to be able to read raw brackets."""
    clean_text = js_text.replace("var morematchmx = ", "").replace(";", "")
    return json.loads(clean_text)

def _clean_data(data_list, dob):
    """Cleans the data (match male vs female)"""
    df = pd.DataFrame(data_list)
    is_male = len(df.columns) > 30 # male arrays: 47 columns vs females: 27
    
    df = df[[0, 4, 16]].copy()
    df.columns = ["match_date", "result", "opp_info"]
    df['result'] = df['result'].map({'W': 'Match won', 'L': 'Match lost'})
    
    df['match_date'] = pd.to_datetime(df['match_date'], format='%Y%m%d', errors='coerce')
    df['player_age'] = (df['match_date'] - pd.to_datetime(dob)).dt.days / 365.25
    
    # Note: female files have opponent DOB vs male files have exact opponent age
    if is_male:
        df['opp_age'] = pd.to_numeric(df['opp_info'], errors='coerce')
    else:
        df['opp_dob'] = pd.to_datetime(df['opp_info'], format='%Y%m%d', errors='coerce')
        df['opp_age'] = (df['match_date'] - df['opp_dob']).dt.days / 365.25
        
    df['age_diff'] = df['player_age'] - df['opp_age']
    return df.dropna(subset=['player_age', 'age_diff'])
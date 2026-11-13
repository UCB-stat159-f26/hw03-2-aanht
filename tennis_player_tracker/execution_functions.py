import requests
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#-----------------------#
# Helper Functions
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
    """
	Strips JavaScript variables to be able to read raw brackets.
	"""
    clean_text = js_text.replace("var morematchmx = ", "").replace(";", "")
    return json.loads(clean_text)

def _clean_data(data_list, dob):
    """
	Cleans the data (match male vs female)
	"""
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

#-----------------------#
# Public Functions
def get_player_data(player_name):
    """
	Takes a name and fetches corresponding cleaned data.
	"""
    
	# removes space(s) in the name 
    clean_name = player_name.title().replace(" ", "")
    
    # dictionary of player DOBs 
    dobs = {"SerenaWilliams": "1981-09-26", "RafaelNadal": "1986-06-03"}
    if clean_name not in dobs:
        raise ValueError(f"'{player_name}' DOB not in database (update the dictionary).")
        
    raw_js = _fetch_js(clean_name)
    data_list = _parse_js(raw_js)
    return _clean_data(data_list, dobs[clean_name])

def plot_player_data(df):
    """Takes a dataframe and generates a scatterplot."""
    fig, ax = plt.subplots(figsize=(13, 7))
    
    sns.scatterplot(data=df, x="player_age", y="age_diff", hue="result", 
					palette={"Match won": "#00A0D1", "Match lost": "#7D2C79"}, s=25, alpha=0.6, edgecolor="none", zorder=2)

	# match the aesthetic of the NYT graphic
    # add center line and despine
    ax.axhline(0, color='gray', linewidth=1, zorder=1, alpha=0.8)
    [spine.set_visible(False) for spine in ax.spines.values()]
    
    # axes, grid, labels, etc.
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.set(ylim=(-24, 24), xlabel="", ylabel="")
    ax.grid(True, color='#eaeaea', linestyle='-', linewidth=0.8, zorder=0)
    ax.tick_params(colors='gray', length=0)
    
    ax.set_yticklabels(["-20", "-10", "Same age", "+10", "+20 years"], color='gray', fontsize=9)
    
    plt.title("Career Matches by Age Difference", fontsize=16, fontweight='bold', pad=40)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2, frameon=False, fontsize=10)
    
    return fig
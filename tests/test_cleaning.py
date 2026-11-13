import pandas as pd
from tennis_player_tracker.execution_functions import _parse_js, _clean_data

def test_female_data_cleaning():
    """
	Tests that female data correctly parses the opponent DOB and calculates age.
	"""
    
    # mock female JS string
    mock_female_js = """var morematchmx = [["19951030", "Canadian Open", "Carpet", "W", "L", "", "", "WC", "Q1", "6-1 6-1", "3", "Anne Miller", "149", "7", "", "R", "19770119", "", "USA", "0", "", "", "", "", "", "", "1995-W-WT-CAN-02A-1995-013"], ["19970307", "Indian Wells", "Hard", "W", "L", "", "", "WC", "Q1", "6-4 6-0", "3", "Alexia Dechaume Balleret", "87", "", "", "R", "19700503", "", "FRA", "0", "", "", "", "", "", "", "1997-W-WT-USA-02A-1997-006"],["19970804", "Manhattan Beach", "Hard", "W", "L", "", "", "WC", "Q3", "7-6 4-6 6-3", "3", "Magui Serna", "54", "6", "", "L", "19790301", "167", "ESP", "0", "", "", "", "", "", "", "1997-W-WT-USA-07A-1997-026"]]"""
    
    # run mock string through the private helper functions
    parsed_list = _parse_js(mock_female_js)
    df = _clean_data(parsed_list, dob="1981-09-26") # Using Serena's DOB
    
    # assertions/tests
    assert len(df) == 3, "DataFrame should have exactly 3 rows"
    assert 'opp_dob' in df.columns, "Female dataset must create an 'opp_dob' column"
    assert df['result'].iloc[0] == "Match lost", "Result mapping failed"

def test_male_data_processing():
    """
	Tests that male data does NOT calculate age and instead, extracts the pre-calculated age.
	"""
    
    # mock male JS string 
    mock_male_js = """var morematchmx = [["20010910", "Spain F10", "Hard", "S", "L", "", "", "WC", "R32", "2-6 7-5 6-2", "3", "Guillermo Platel", "731", "", "", "R", "22.264202601", "", "ESP", "0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "2001-M-FU-ESP-10A-2001-002", "", "1", "1"], ["20010917", "Seville CH", "Clay", "C", "L", "", "", "WC", "R16", "3-6 6-1 6-3", "3", "Stefano Galvani", "161", "2", "", "R", "24.2902121834", "178", "ITA", "0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "2", "", "", "", "2001-784-024", "", "2", "2"], ["20010917", "Seville CH", "Clay", "C", "W", "", "", "WC", "R32", "6-4 6-4", "3", "Israel Matos Gil", "751", "", "Q", "U", "18.7597535934", "", "ESP", "0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "2001-784-015", "", "1", "1"]]"""
    
    # run the mock string throughthe private helper functions
    parsed_list = _parse_js(mock_male_js)
    df = _clean_data(parsed_list, dob="1986-06-03") # Using Rafael's DOB
    
    # assertions/tests
    assert len(df) == 3, "DataFrame should have exactly 3 rows"
    assert 'opp_dob' not in df.columns, "Male dataset should NOT have an 'opp_dob' column"
    assert df['opp_age'].iloc[0] == 22.264202601, "Failed to extract exact male opponent age"
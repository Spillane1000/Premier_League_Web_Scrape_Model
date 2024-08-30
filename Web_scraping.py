# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
from bs4 import BeautifulSoup
import requests
import urllib.parse


WHU_df = 'https://fbref.com/en/squads/7c21e445/2022-2023/West-Ham-United-Stats'


def get_match_reports(team_url):
    
    response = requests.get(team_url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')  # Find all <a> tags
    urls = [link.get('href') for link in links if link.get('href')]
    
    
    absolute_urls = []
    for url in urls:
        full_url = urllib.parse.urljoin(response.url, url)  # Convert relative URL to absolute
        if "matches" in url:
            absolute_urls.append(full_url)
            
    return absolute_urls

WHU_match_reports = get_match_reports(WHU_df)
match_report_url = WHU_match_reports[1]

def get_squad_info(match_report_url):
   
    home_squad = pd.read_html(match_report_url)[0]
    away_squad = pd.read_html(match_report_url)[1]
    
    home_squad = home_squad.iloc[:,1]
    away_squad = away_squad.iloc[:,1]
    
    home_player_stats = pd.read_html(match_report_url)[3]
    away_player_stats = pd.read_html(match_report_url)[10]
    
    home_player_stats.columns = home_player_stats.columns.droplevel()
    away_player_stats.columns = away_player_stats.columns.droplevel()
    
    result = {"home_starting":home_squad,"away_starting":away_squad,
            "home_stats":home_player_stats,"away_stats":away_player_stats}

    return result

print(get_squad_info(match_report_url))


#df.columns = df.columns.droplevel()
#print(df)


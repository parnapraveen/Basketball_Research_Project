#!/usr/bin/env python3

import pandas as pd
from bs4 import BeautifulSoup
import requests
import os.path

#########################
# years - list of numerical values indicating year of data to collect for players
#########################
def get_bb_data(years):
    header = ["Rk", "Player", "Pos", "Age", "Tm", "G", "GS", "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "2P", "2PA", "2P%", "eFG%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]
    
    for year in years:
        year = str(year)
        fname = 'data/basketball-ref' + year + '.csv'
        if not os.path.isfile(fname):
            url = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) + '_totals.html'
        
            data = []
            
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            rk = 0
            p = ""
            table = soup.find('table')
            for row in table.tbody.find_all("tr"):
                col = row.find_all("td")
            
                if col != []:
                    name = col[0].text.strip()
                    if p != name:
                        rk += 1
                        p = name
                    data.append([rk] + [i.text.strip() for i in col])
            
            df = pd.DataFrame(data)
            df = df.set_axis(header, axis=1)
            
            df.to_csv(fname)

#get_bb_data(range(2000,2025))

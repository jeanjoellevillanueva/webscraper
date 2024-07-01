import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://www.basketball-reference.com/leagues/NBA_2024_per_game.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table', id='per_game_stats')
headers = [th.text.strip() for th in table.find_all('th', scope='col')]
rows = []
for tr in table.find_all('tr', class_='full_table'):
    rows.append([td.text.strip() for td in tr.find_all('td')])

df = pd.DataFrame(rows, columns=headers[1:])
numeric_columns = [
    'Age',
    'G',
    'GS',
    'MP',
    'FG',
    'FGA',
    'FG%',
    '3P',
    '3PA',
    '3P%',
    '2P',
    '2PA',
    '2P%',
    'eFG%',
    'FT',
    'FTA',
    'FT%',
    'ORB',
    'DRB',
    'TRB',
    'AST',
    'STL',
    'BLK',
    'TOV',
    'PF',
    'PTS'
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.sort_values('PTS', ascending=False)
df.to_excel('nba_player_stats.xlsx', index=False)

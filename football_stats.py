import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://www.soccerstats.com/matches.asp?matchday=1#'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a', text = 'stats')

filtered_links = []
for link in links:
    if 'stats' in link['href']:
        filtered_links.append(link['href'])
        print(link['href'])



tables = {}
for count, link in enumerate(filtered_links, start = 1):
    try:
        html = requests.get('https://www.soccerstats.com/' + link, headers=headers).text
        soup = BeautifulSoup(html, 'html.parser')
        
        goalsTable = soup.find('h2', text='Goal statistics')
        
        teams = goalsTable.find_next('table')
        teamsStr = teams.find_all('td')[0].text + ' ' + teams.find_all('td')[-1].text
        
        goalsTable = teams.find_next('table')
        df = pd.read_html(str(goalsTable))[0]
        
        # print(f'{count} of {len(filtered_links)}: {teamsStr}')
        tables[teamsStr] = df
        
    except Exception as e:
        print(e)
        print(f'{count} of {len(filtered_links)}: {teamsStr} !! NO GOALS STATISTICS !!')


import requests
import pandas as pd
from bs4 import BeautifulSoup

### Time is based on UK Time for soccerstats.com
# Today's Matches
url = 'https://www.soccerstats.com/matches.asp?matchday=1#'

# Tomorrow's Matches
#url = 'https://www.soccerstats.com/matches.asp?matchday=2&daym=tomorrow'

# Headers and response from statistics website
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
response = requests.get(url, headers = headers)

# Use Soup to gather links and data
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a', class_ = 'myButton', text = 'stats')

# Leagues to get stats from
# leagues = ['spain&', 'england&', 'italy&', 'france&', 'germany&']
leagues = ['spain&']
filtered_links = [link['href'] for link in links if any(league in link['href'] for league in leagues)]

########## Get the stats page for all leagues
stats_tables = ['Contextual averages', 'Scoring rates', 'Home vs Away Stats']
### TO-DO
### One by one, can't generalize

# Dictionary to store scraped data
matches_data = {}

#### Getting different stats

# Iterate through filtered links
for link in filtered_links:
    try:
        # Fetch HTML content
        response = requests.get('https://www.soccerstats.com/' + link, headers = headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the match identifier or name
        match_name = soup.find('h1').text.strip()

        # Initialize the dictionary for this match
        matches_data[match_name] = {}

        # Contextual averages
        header = soup.find('h2', text = 'Contextual averages')
        table = header.find_next('table')



        # for stat_category in stats_tables:
        #     # Find the table by category
        #     header = soup.find('h2', text = 'Contextual averages')
        #     if header:
        #         table = header.find_next('table')
        #         if table:
        #             df = pd.read_html(str(table))[0]
        #             matches_data[match_name][stat_category] = df
        #         else:
        #             print(f"Table for {stat_category} not found in {link}")
        #     else:
        #         print(f"Category {stat_category} not found in {link}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {link}: {e}")
    except ValueError as e:
        print(f"Error parsing HTML for {link}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for {link}: {e}")


# Example of accessing the scraped data
print(matches_data)
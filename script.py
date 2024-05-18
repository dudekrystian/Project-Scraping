from bs4 import BeautifulSoup
import requests
import pandas as pd

# create table for all clubs and anothe list to clubs selected.

timetable_list = []
list_clubs= ['Liverpool FC', 'FC Arsenal', 'Manchester City', 'Aston Villa', 'Manchester United', 'Newcastle Unite', 'FC Chelsea', 'Tottenham Hotspur']

# get data from page URL and use loop to scraping any webiste.

for i in range(1,39):
    url = ('https://www.kicktipp.pl/info/serwis/zawody/premier%20league%20(eng)/spielplan?saisonId=201825&spieltagIndex=')
    index = str(i)

    full_url = url + index

    page_to_scrape = requests.get(full_url)

    soup = BeautifulSoup(page_to_scrape.text, "html.parser")

    rows = soup.find('table', {'id': 'spiele'}).find('tbody').find_all('tr')

    for row in rows:
        dic = {}
        dic['StartDate'] = row.find_all('td')[0].text
        dic['Home'] = row.find_all('td')[1].text
        dic['Away'] = row.find_all('td')[2].text
        dic['Result'] = row.find_all('td')[3].text

        timetable_list.append(dic)

# use pandas with DataFrame and format column with data.
df = pd.DataFrame(timetable_list)
df['StartDate'] = pd.to_datetime(df['StartDate'], format='%d.%m.%y %H:%M' )

list_to_sorting = []

# transform data and sorting.

for i in range(0,8):
    club = df[df[['Home', 'Away']].isin([list_clubs[i], list_clubs[i]]).any(axis=1)]
    club['Club'] = str(list_clubs[i])
    club = club.sort_values(by=['StartDate'])
    club['EndDate'] = club['StartDate'].shift(-1) 
    club['Duration [days]']  = club['EndDate'] - club['StartDate']
    club['Duration [hours]']  = club['Duration [days]'].dt.total_seconds()/(3600.0)
    list_to_sorting.append(club)
    
sorting_list_clubs = pd.concat(list_to_sorting)

# views example
print(sorting_list_clubs)

# save to file
sorting_list_clubs.to_excel('report_average_time.xlsx', index=False)
sorting_list_clubs.to_csv('report_average_time.csv', index=False)
import re

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://tf.tfrrs.org/list_data/3711?other_lists=https%3A%2F%2Fxc.tfrrs.org%2Flists%2F3711%2F2022_NCAA_Division_I_Outdoor_Qualifying_FINAL&limit=500&event_type=19&year=&gender=m"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

table = soup.find("table")

rows = []
count = 0
for row in table.find_all("tr"):
    name_cell = row.find('td', {'class': re.compile('tablesaw-priority-1')})
    str_name_cell = str(name_cell)
    athlete_url_ = re.findall(r'(https?://\S+)', str_name_cell)
    if len(athlete_url_) > 0:
        athlete_url = athlete_url_[0].split('"')
    else:
        continue
    athlete_response = requests.get(athlete_url[0])
    athlete_soup = BeautifulSoup(athlete_response.content, "html.parser")
    time_cells = athlete_soup.find_all("td")
    time800 = time_cells[11].text.replace("\n", "")
    time1500 = time_cells[13].text.replace("\n", "")
    timeMile = time_cells[15].text.replace("\n", "")
    time3000 = time_cells[7].text.replace("\n", "")
    time5000 = time_cells[9].text.replace("\n", "")
    rows.append([time800, time1500, timeMile, time3000, time5000])

df = pd.DataFrame(rows, columns=["Time800", "Time1500", "TimeMile", "Time3000", "Time5000"])
print(df.head())
df.to_csv('5k.csv', index=False, sep=',')

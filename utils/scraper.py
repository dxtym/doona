import requests
from bs4 import BeautifulSoup

response = requests.get('https://intranet.wiut.uz/TimeTableNew/GetLessons')
soup = BeautifulSoup(response.text, 'html.parser')

classes = soup.find_all('div', {'class': 'inner_box', id: 'Monday'})
print(classes)
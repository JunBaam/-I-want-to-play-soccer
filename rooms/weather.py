from bs4 import BeautifulSoup
import requests
from pprint import pprint


def get_weather():
    district = "용산구"
    html = requests.get('https://search.naver.com/search.naver?query=날씨' + district)
    soup = BeautifulSoup(html.text, 'html.parser')
    data1 = soup.find('div', {'class': 'weather_box'})
    find_address = data1.find('span', {'class': 'btn_select'}).text
    return find_address





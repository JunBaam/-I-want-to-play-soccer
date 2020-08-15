from bs4 import BeautifulSoup
import requests


district = "용산구"

html = requests.get('https://search.naver.com/search.naver?query=날씨' + district)


soup = BeautifulSoup(html.text, 'html.parser')

data1 = soup.find('div', {'class': 'weather_box'})


find_address = data1.find('span', {'class': 'btn_select'}).text
print('현재 위치: ' + find_address)


find_currenttemp = data1.find('span', {'class': 'todaytemp'}).text
print('현재 온도: ' + find_currenttemp + '℃')

find_currentstate = data1.find('p', {'class': 'cast_txt'}).text
print('현재 상태: ' + find_currentstate)

data2 = data1.findAll('dd')

find_dust = data2[0].find('span', {'class': 'num'}).text
find_ultra_dust = data2[1].find('span', {'class': 'num'}).text

print('현재 미세먼지: ' + find_dust)
print('현재 초미세먼지: ' + find_ultra_dust)

# existing_file.html 은 너가 넣고 싶은 html 파일명 넣기
with open("room_detail.html") as inf:
    txt = inf.read()
    soup = BeautifulSoup(txt)

# create new link
new_div = soup.new_tag('div', id='너가 원하는 id')
new_div.string = '현재 미세먼지: ' + find_dust
new_div2 = soup.new_tag('div', id='너가 원하는 id')
new_div2.string = '현재 초미세먼지: ' + find_ultra_dust

soup.body.append(new_div)
soup.body.append(new_div2)

# save the file again
with open("room_detail.html", "w") as outf:
    outf.write(str(soup))
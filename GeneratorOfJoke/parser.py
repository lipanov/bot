import requests
from bs4 import BeautifulSoup
link ="https://www.anekdotovmir.ru/anekdoty-bez-mata-i-plohih-slov/"
link1 ="https://vseanekdoty.ru/bez-mata/"
responce = requests.get(link).text

soup = BeautifulSoup(responce, 'lxml')
content = soup.find('article' , id = "post-136312")
check_content = ""


p = content.find_all('p')
p_count = len(p)



for i in range(0, p_count):
 check_content = check_content + content.find_all('p')[i].text + "\n"


responce1 = requests.get(link).text
soup = BeautifulSoup(responce1, 'lxml')
content1 = soup.find('div' , id = "content")
p1 = content1.find_all('p')
p1_count = len(p1)

for i in range(0, p1_count):
 check_content = check_content + content1.find_all('p')[i].text + "\n"

with open('Some.txt' , 'w')  as file_handler:
 file_handler.write(check_content)
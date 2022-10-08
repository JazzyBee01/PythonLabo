import requests
from bs4 import BeautifulSoup
import datetime

url = "https://tradingeconomics.com/commodity/eu-natural-gas"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

req = requests.get(url, headers = headers)
result = req.content
print(result[:100])

soup = BeautifulSoup(result, 'html.parser')
#kader onderaan de pagina
div = soup.find(id = "ctl00_ContentPlaceHolder1_ctl00_ctl01_Panel1")
td = div.find_all('td')
#cel met dagprijs in EUR/MWh
dagprijs = td[1].text

print(dagprijs)

with  open('1_Energiecrisis/gecheckteData.csv', "a") as f:
	f.write(f'{datetime.date.today()}, {dagprijs}\n')


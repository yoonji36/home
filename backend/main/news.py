import requests
from bs4 import BeautifulSoup

# 오픈 API를 사용하여 최신 뉴스 데이터 가져오기
url = 'https://newsapi.org/v2/top-headlines'
params = {
    'country': 'us',
    'apiKey': 'your_api_key'
}
response = requests.get(url, params=params)
data = response.json()

# 웹 크롤링을 사용하여 추가적인 뉴스 수집
url = 'https://example-news-website.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 수집된 뉴스 데이터 저장 및 제공
news_data = []
for article in data['articles']:
    news_data.append(article['title'])
for headline in soup.find_all('h2', class_='headline'):
    news_data.append(headline.text)

for news in news_data:
    print(news)
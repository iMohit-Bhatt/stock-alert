import requests
import datetime as dt
from twilio.rest import Client
STOCK = "tsla"
COMPANY_NAME = "TESLA"

account_sid = "[your accound sid]"
auth_token = "[your auth token]"
stock_endpoint = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey=[your api key]"
news_endpoint = "https://newsapi.org/v2/everything?q=tesla&apiKey=[your api key]"

stock_response = requests.get(url=stock_endpoint)
stock_data = stock_response.json()['Time Series (Daily)']

stock_data_list = [value for (key, value) in stock_data.items()]

yesterday_data = stock_data_list[0]
yesterday_closing_prize = yesterday_data['4. close']

day_before_yesterday = stock_data_list[1]
day_before_yesterday_closing_prize = day_before_yesterday['4. close']

diff = float(yesterday_closing_prize) - float(day_before_yesterday_closing_prize)
up_down = None
if diff > 0:
    up_down = "🔺"
else: 
    up_down = "🔻"

diff_percent = (abs(diff)/float(yesterday_closing_prize)) * 100
diff_percent = round(diff_percent)

if diff_percent > 0.5:
    news_response = requests.get(url=news_endpoint)
    news_data = news_response.json()["articles"]
    news = news_data[:3]

    formatted_article = [f" TESLA: {up_down}{diff_percent}% \nHeadline: {new['title']}.\nBrief: {new['description']}" for new in news]

    client = Client(account_sid, auth_token)
    for article in formatted_article:
        message = client.messages.create(
            body=article,
            from_='senders number',
            to='recivers number'
        )
    print(message.status)

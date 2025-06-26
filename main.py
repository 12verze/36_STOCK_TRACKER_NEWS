from pyexpat.errors import messages
from twilio.rest import Client
import requests

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY_STOCK = "H44FPDSOVDKAMAKJ"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://gnews.io/api/v4/search"
API_KEY_NEWS = 'ea12afc2f9b1807bc176b7ea5b1412ae'

Account_SID = "ACaa2c78e0144afa8049491beac790b52d"
Auth_token = "cb6065d88a4e8facb3f992609cb61027"


parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
"outputsize": "compact",
    "apikey": API_KEY_STOCK
}

response = requests.get(STOCK_ENDPOINT,params=parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]


first_date = list(data.keys())[0]
first_closing_price = float(data[first_date]["4. close"])
second_date = list(data.keys())[1]
second_closing_price = float(data[second_date]["4. close"])

stock_rise = round(abs(first_closing_price-second_closing_price)*100/first_closing_price,2)

if first_closing_price >second_closing_price:
    emoji = "🔺"
else:
    emoji ="🔻"

params = {
    "q": "tesla OR elon musk OR stocks",
    "lang": "en",
    "country": "us",
    "max": 3,
    "apikey": API_KEY_NEWS,
    "from":first_date
}
response2 = requests.get(NEWS_ENDPOINT,params= params)
response2.raise_for_status()
news = response2.json()["articles"]
msgs = [f"{COMPANY_NAME} {emoji}{stock_rise}%\n"
       f"{x["title"]} - [{x["source"]["name"]}]\n"
       f"Read at - {x["url"]}" for x in news ]


if stock_rise>=3.5:
    for m in msgs:
        client = Client(Account_SID, Auth_token)
        message = client.messages.create(
            body=f"{m}",
            from_ = "whatsapp:+14155238886",
            to="whatsapp:+919358186576",
        )
        print(message.status)

##tip: twilio sandbox expires every 24hr so u have to reactivate it to get msgs


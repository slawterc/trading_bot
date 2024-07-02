import requests
from ai_util import estimate_sentiment

class REST():
    def __init__(self, ALPACA_CREDS:dict):
        self.creds = ALPACA_CREDS
        self.headers = {
            "accept": "application/json",
            "APCA-API-KEY-ID": self.creds['API_KEY'],
            "APCA-API-SECRET-KEY": self.creds['API_SECRET']
        }
        self.base_url = "https://data.alpaca.markets/v1beta1/"

    def get_headlines(self, start:str, end:str, symbol:str) -> list:
        url = (f"{self.base_url}news?start={start}&end={end}&sort=desc&symbols={symbol}&include_content=false")
        headers = self.headers
        response = requests.get(url, headers=headers)
        res_json = response.json()

        headlines = []

        for n in res_json['news']:
            headlines.append(n["headline"])

        return headlines
    
    def get_top_movers(self, limit:int) -> dict:
        url = (f"{self.base_url}screener/stocks/movers?top={limit}")
        headers = self.headers
        response = requests.get(url, headers=headers)
        movers = response.json()
        return movers
    
    def get_most_active(self, limit:int) -> dict:
        url = (f"{self.base_url}screener/stocks/most-actives?by=volume&top={limit}")
        headers = self.headers
        response = requests.get(url, headers=headers)
        most_active = response.json()
        return most_active

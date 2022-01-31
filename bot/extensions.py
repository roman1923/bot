import json
import requests
from config import exchanges

class APIException(Exception):
    pass

class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_key}&tsyms={base_key}')
        answer = json.loads(r.content)
        message =  f"Цена {amount} {base} в {quote} : {answer}"
        return message
        

    
__author__ = 'akashjeez'

import os, sys, json, requests
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from fake_useragent import UserAgent

app = Flask(__name__)
headers = {'User-Agent': UserAgent().random}

@app.route('/')
def index():
	return "Index Page!"

@app.route('/about')
def about():
	return "About Page!"


def GetBitcoinData(category, timeline):
	try:
		dataset, BASE_URL = [], 'https://api.blockchain.info/charts/{}?timespan={}&format=json'
		if category == 'market-price':
			response = requests.get(BASE_URL.format('market-price', timeline), headers = headers).json()
		elif category == 'blocks-size':
			response = requests.get(BASE_URL.format('blocks-size', timeline), headers = headers).json()
		else:
			response = {'error': "Invalid Category!"}
	except Exception as ex:
		return f"Error: {ex}"

@app.route('/bitcoin/price', methods = ['GET', 'POST'])
def bitcoin_price():
	try:
		dataset, BASE_URL = [], 'https://api.blockchain.info/charts'
		category = request.args.get('category', default = 'market-price', type = str)
		timespan = request.args.get('timespan', default = '30days', type = str)
		if category.casefold() == 'market-price':
			response = requests.get(f"{BASE_URL}/market-price?timespan={timespan}&format=json", headers = headers).json()
		elif category.casefold() == 'blocks-size':
			response = requests.get(f"{BASE_URL}/blocks-size?timespan={timespan}&format=json", headers = headers).json()
		return jsonify(results = {
			'name': response.get('name', 'TBD'), 
			'unit': response.get('unit', 'TBD'), 
			'period': response.get('period', 'TBD'), 
			'description': response.get('description', 'TBD'),
			'data': [{'date': datetime.fromtimestamp(data['x']).strftime('%d-%m-%Y'), 'value': data.get('y', 0)} for data in response['values']]
		}), 200
	except Exception as ex:
		return f"""Error: {ex} <br/> Something Went Wrong! Please Visit <a href='https://www.blockchain.com/api/' 
			target='_blank'> Bitcoin API Site! </a>"""

@app.route('/bitcoin/exchange', methods = ['GET', 'POST'])
def bitcoin_exchange():
	try:
		dataset, BASE_URL = [], 'https://api.blockchain.info'
		code = request.args.get('code', default = 'USD', type = str)
		value = request.args.get('value', default = 500, type = int)
		response_1 = requests.get(f"{BASE_URL}/ticker", headers = headers).json()
		response_2 = requests.get(f"{BASE_URL}/tobtc?currency={code.upper()}&value={str(value)}", headers = headers).json()
		return jsonify(results = { 
			'count': len(response_1), 'data': response_1 , 
			'from_currency': code.upper(),'to_currency': 'BTC', 
			'value': int(value), 'price': response_2
		}), 200
	except Exception as ex:
		return f"""Error: {ex} <br/> Something Went Wrong! Please Visit <a href='https://www.blockchain.com/api/exchange_rates_api' 
			target='_blank'> Bitcoin Exchange Rates API Site! </a>"""


if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 4321, debug = True)
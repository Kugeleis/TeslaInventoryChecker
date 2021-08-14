import argparse
import json
import configparser
import os
import http.client
import urllib
import time
import discord
from datetime import datetime
from types import SimpleNamespace

parser = argparse.ArgumentParser(
    description='Search and get notified for Tesla Inventory')
parser.add_argument(
    '-c', '--config', help='Override Configuration File by providing file name in current directory, e.g. m3.ini')
parser.add_argument(
    '-r', '--repeat', help='Repeat this every x seconds. Suggested = 60')
parser.add_argument(
    '-dt', '--discordtest', action='store_true', help='Sends test message to Discord on start-up.')

args = parser.parse_args()

current_dir = os.path.dirname(__file__)
config_file = os.path.join(current_dir, 'config.ini')
if args.config != None:
    config_file = os.path.join(current_dir, args.config)

config = configparser.ConfigParser()
config.read(config_file)
model = config['Inventory']['model']
region = config['Inventory']['region']
market = config['DEFAULT']['market']
zipcodes = config['Inventory']['zip'].split(",")
coordinates = config['Inventory']['lat_long'].split(";")
zip_range = config['DEFAULT']['range']
condition = config['DEFAULT']['condition']

if args.discordtest:
    discord.send_test_message(config['Discord']['api'], "Initiating Tesla Vehicle Inventory Search ...")

while True:
    for i in range(len(zipcodes)):
        zipcode = zipcodes[i]
        print(
            f'Searching for {condition} Tesla {model.upper()} within {zip_range} miles of {zipcode}')

        lat = float(coordinates[i].split(",")[0])
        lng = float(coordinates[i].split(",")[1])

        search_query = {
            "query": {
                "model": model,
                "condition": condition,
                "options": {},
                "arrangeby": "Price",
                "order": "asc",
                "market": market,
                "language": "en",
                "super_region": config['DEFAULT']['super_region'],
                "lng": lng,
                "lat": lat,
                "zip": zipcode,
                "range": int(zip_range),
                "region": region
            },
            "offset": 0,
            "count": 50,
            "outsideOffset": 0,
            "outsideSearch": False
        }

        api_path = "/inventory/api/v1/inventory-results?query=" + \
            urllib.parse.quote_plus(json.dumps(search_query))
        base_search_url = "https://www.tesla.com"
        if market == "CA":
            base_search_url += "/en_CA"
        search_url = f'{base_search_url}/inventory/{condition}/{model}?arrangeby=phl&zip={zipcode}&range={zip_range}'
        conn = http.client.HTTPSConnection("www.tesla.com")
        payload = ''
        headers = {
            'Referer': search_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'dnt': '1'
        }

        try:
            conn.request("GET", api_path, payload, headers)
            res = conn.getresponse()
            data = res.read()
            search_results = json.loads(
                data, object_hook=lambda d: SimpleNamespace(**d))
        except Exception as e:
            print(f'Error calling Tesla API\n{str(e)}')
            continue

        total_matches = int(search_results.total_matches_found)
        total_exact = 0
        total_approximate = 0
        total_approximateOutside = 0

        try:
            if type(search_results.results) is not list:
                total_exact = len(search_results.results.exact)
                total_approximate = len(search_results.results.approximate)
                total_approximateOutside = len(
                    search_results.results.approximateOutside)

            total_split_matches = total_exact + total_approximate + total_approximateOutside
        except:
            print(f"Error parsing Tesla Response:\n{str(e)}\n---")
            continue

        try:
            if total_matches > 0:
                print(
                    f"Inventory Found - {str(total_matches)} {condition} {model} found at {datetime.now()}")
                discord.send_message(config['Discord']['api'], json.loads(
                    (json.dumps(search_query)), object_hook=lambda d: SimpleNamespace(**d)), search_results)
            elif total_split_matches > 0:
                print(
                    f"Split Inventory Found - {str(total_split_matches)} {condition} {model} found at {datetime.now()}")
                discord.send_message_split_results(config['Discord']['api'], json.loads(
                    (json.dumps(search_query)), object_hook=lambda d: SimpleNamespace(**d)), search_results)
            else:
                print(
                    f"No {condition} {model} vehicles were found at {datetime.now()}")
        except Exception as e:
            print(f"Error sending message to discord:\n{str(e)}\n---")
            continue

    if args.repeat == None:
        break
    else:
        print(f">> Waiting for {args.repeat} seconds ...")
        time.sleep(int(args.repeat))

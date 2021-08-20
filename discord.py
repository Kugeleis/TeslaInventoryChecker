import json
import http.client
import urllib
import helper
import time
from tinydb import Query

referral_code = "christina37902"

def get_model_name(model):
    if model == "m3":
        return "model3"
    elif model == "my":
        return "modely"
    elif model == "ms":
        return "models"
    elif model == "mx":
        return "modelx"
    else:
        return model


def build_vehicle_card(v, search_query):
    desc = f"→ VIN: {v.VIN}\n"
    try:
        desc += f"→ Odometer: {str(v.Odometer)} {v.OdometerType}\n"
        desc += f"→ Price: {str(v.Price)}\n"
        if v.CountryCode == "US":
            desc += f"→ Sticker Price: {str(v.MonroneyPrice)}\n"
        desc += f"\n→ Exterior: {helper.list_to_string(v.PAINT)}\n"
        desc += f"→ Interior: {helper.list_to_string(v.INTERIOR)}\n"
        try:
            desc += f"→ Wheels: {helper.list_to_string(v.WHEELS)}\n"
            desc += f"→ Additional Options: {helper.list_to_string(v.ADL_OPTS)}\n"
            desc += f"→ Autopilot: {helper.list_to_string(v.AUTOPILOT)}\n"

            if v.InTransit:
                desc += f"\n→ In-Transit"
            if v.IsAvailableForMatch is not True:
                desc += f"\n→ Vehicle Is NOT Available For Match"
            if v.IsDemo:
                desc += f"\n→ Demo Vehicle"
            if v.IsSoftMatched:
                f"\n→ Already Soft Matched"
            desc += f"\n→ Listing Type: {v.ListingType}\n"
            desc += f"→ Last Updated: {helper.try_parse_date_time(v.DocumentSyncDate, -4)} EDT\n"
            desc += f"→ Factory Gate Date: {helper.try_parse_date_time(v.ActualGAInDate, -4)} EDT\n"
            if v.NeedsReview:
                desc += f"→ Listing/Vehicle Needs Review\n"
        except Exception as ex:
            print(f"Extra data points failed for current vehicle - {str(ex)}")
        desc += f"\n→ Location: {v.City}, {v.StateProvince}, {v.CountryCode}"
    except Exception as e:
        print(f'error building description for vehicle - {str(e)}')

    embeds = [
        {
            "title": "View Listing Page",
            "description": desc,
            "url": f"{get_base_url(search_query.query.market)}/{v.Model}/order/{v.VIN}?referral={referral_code}&postal={urllib.parse.quote(search_query.query.zip)}",
            "footer": {
                "text": "Note: If this link redirects you to the inventory search page, the vehicle is no longer available."
            }
        },
        {
            "title": f"Reserve this {helper.list_to_string(v.PAINT)} {v.Model.upper()} {v.TrimName}",
            "url": f"{get_base_url(search_query.query.market)}/{get_model_name(v.Model)}/order/{v.VIN}?referral={referral_code}&postal={urllib.parse.quote(search_query.query.zip)}#payment",
            "footer": {
                "text": "Note: If this link returns an error, this vehicle is no longer available. Good luck!"
            }
        },
    ]

    card = {
        "content": f"{v.Year} {v.Model.upper()} {v.TrimName} - {helper.list_to_string(v.PAINT)}",
        "embeds": embeds
    }

    return card


def get_base_url(market):
    base_url = "https://www.tesla.com"
    if market == "CA":
        base_url += "/en_CA"
    return base_url


def build_search_url(search_query):
    return f"{get_base_url(search_query.query.market)}/inventory/{search_query.query.condition}/{search_query.query.model}?arrangeby=phl&referral={referral_code}&zip={urllib.parse.quote(search_query.query.zip)}&range={str(search_query.query.range)}"


def send_test_message(api_key, message):
    msg = {
        "content": message
    }

    conn = http.client.HTTPSConnection("discord.com")
    payload = json.dumps(msg)
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", api_key, payload, headers)
    res = conn.getresponse()
    print(f'Discord Message Send Status: {res.status} {res.reason}')
    if (res.status != 204):
        print(payload)
        raise ValueError(
            'Discord Message Failed to send. Please check your configuration.')


def send_search_listing(api_key, search_query, total_matches):
    msg = {
        "content": f"{str(total_matches)} {search_query.query.condition} {search_query.query.model.upper()} found within {search_query.query.range} miles of {search_query.query.zip} in {search_query.query.region}",
        "embeds": [
            {
                "title": f"View all {search_query.query.model.upper()} inventory near {search_query.query.zip}",
                "description": "This link will take you to Tesla's inventory search page.",
                "url": build_search_url(search_query),
                "color": None
            }
        ]
    }

    conn = http.client.HTTPSConnection("discord.com")
    payload = json.dumps(msg)
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", api_key, payload, headers)
    res = conn.getresponse()
    print(f'Discord Message (Search Listing) Send Status: {res.status} {res.reason}')
    if res.status != 204:
        print("Failed to send message to Discord")
        print(payload)


def send_vehicle_found_message(api_key, search_query, vehicle):
    conn = http.client.HTTPSConnection("discord.com")
    payload = json.dumps(build_vehicle_card(vehicle, search_query))
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", api_key, payload, headers)
    res = conn.getresponse()
    print(f'Discord Message (VIN: {vehicle.VIN}) Send Status: {res.status} {res.reason}')
    if res.status != 204:
        print("Failed to send message to Discord")
        print(payload)


def parse_vehicle_results(vehicles, db):
    total_matches = len(vehicles)
    new_matches = []
    for x in range(total_matches):
        vin = vehicles[x].VIN
        vehicle = Query()
        vehicle_matches = db.search(vehicle.vin == vin)
        if len(vehicle_matches) > 0:
            print(f'-- Vehicle was previously detected - {vehicle_matches}')
            if vehicle_matches[0]["isAvailable"] == False:
                db.update(set("isAvailable", True), vehicle.vin == vin)
                new_matches.append(vehicles[x])
        else:
            print(f"++ New Vehicle found - {vin}")
            db.upsert({"vin": vin, "isAvailable": True}, vehicle.vin == vin)
            new_matches.append(vehicles[x])
    print(f'total new matches found - {str(len(new_matches))}')
    return new_matches


def send_message(api_key, search_query, vehicles, db):
    new_matches = parse_vehicle_results(vehicles, db)
    total_matches = len(new_matches)

    if total_matches > 0:
        send_search_listing(api_key, search_query, total_matches)
        time.sleep(0.5)

    for x in range(total_matches):
        try:
            send_vehicle_found_message(api_key, search_query, new_matches[x])
            time.sleep(0.5)
        except Exception as e:
            print(f'Error adding vehicle data to search - {str(e)}')

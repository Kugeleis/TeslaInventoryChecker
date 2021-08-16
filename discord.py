import json
import http.client
import urllib
import helper

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
            
            if v.InTransit: desc += f"\n→ In-Transit"
            if v.IsAvailableForMatch is not True: desc += f"\n→ Vehicle Is NOT Available For Match"
            if v.IsDemo: desc += f"\n→ Demo Vehicle"
            if v.IsSoftMatched: f"\n→ Already Soft Matched"
            desc += f"\n→ Listing Type: {v.ListingType}\n"
            desc += f"→ Document Sync Date: {helper.try_parse_date_time(v.DocumentSyncDate, 0)}\n"
            desc += f"→ Factory Gate Date: {helper.try_parse_date_time(v.ActualGAInDate, 0)}\n"
            if v.NeedsReview: desc += f"→ Listing/Vehicle Needs Review\n"
        except Exception as ex:
            print(f"Extra data points failed for current vehicle - {str(ex)}")
        desc += f"\n→ Location: {v.City}, {v.StateProvince}, {v.CountryCode}"
    except Exception as e:
        print(f'error building description for vehicle - {str(e)}')

    card = {
        "title": f"{v.Year} {v.Model.upper()} {v.TrimName} - {helper.list_to_string(v.PAINT)}",
        "description": desc,
        "url": f"{get_base_url(search_query.query.market)}/{v.Model}/order/{v.VIN}?referral=christina37902&postal={urllib.parse.quote(search_query.query.zip)}",
        "color": None
    }

    if v.StateProvince != search_query.query.region:
        print(
            f"Vehicle found does not belong in current State/Region.\n---\n\n{v}\n\n---")
    return card


def get_base_url(market):
    base_url = "https://www.tesla.com"
    if market == "CA":
        base_url += "/en_CA"
    return base_url


def build_search_url(search_query):
    return f"{get_base_url(search_query.query.market)}/inventory/{search_query.query.condition}/{search_query.query.model}?arrangeby=phl&referral=christina37902&zip={urllib.parse.quote(search_query.query.zip)}&range={str(search_query.query.range)}"

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
        raise ValueError('Discord Message Failed to send. Please check your configuration.')

def send_message(api_key, search_query, search_results):
    total_matches = int(search_results.total_matches_found)

    msg = {
        "content": f"{str(total_matches)} {search_query.query.condition} {search_query.query.model.upper()} found within {search_query.query.range} miles of {search_query.query.zip} in {search_query.query.region}",
        "embeds": [
            {
                "title": f"View all {search_query.query.model.upper()} inventory",
                "description": "This link will take you to Tesla's inventory search page.",
                "url": build_search_url(search_query),
                "color": None
            }
        ]
    }

    for x in range(total_matches):
        if x == 9:
            break
        try:
            msg["embeds"].append(build_vehicle_card(search_results.results[x], search_query))
        except Exception as e:
            print(f'Error adding vehicle data to search - {str(e)}')

    conn = http.client.HTTPSConnection("discord.com")
    payload = json.dumps(msg)
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", api_key, payload, headers)
    res = conn.getresponse()
    print(f'Discord Message Send Status: {res.status} {res.reason}')
    if res.status != 204:
        print("Failed to send message to Discord")
        print(payload)

def send_message_split_results(api_key, search_query, search_results):
    total_exact = len(search_results.results.exact)
    total_approximate = len(search_results.results.approximate)
    total_approximateOutside = len(search_results.results.approximateOutside)
    total_split_matches = total_exact + total_approximate + total_approximateOutside

    msg = {
        "content": f"{str(total_split_matches)} {search_query.query.condition} {search_query.query.model.upper()} found within {search_query.query.range} miles of {search_query.query.zip} in {search_query.query.region}",
        "embeds": [
            {
                "title": f"View all {search_query.query.model.upper()} inventory",
                "description": "This link will take you to Tesla's inventory search page.",
                "url": build_search_url(search_query),
                "color": None
            }
        ]
    }

    for x in range(total_exact):
        if len(msg["embeds"]) == 10:
            break

        msg["embeds"].append(build_vehicle_card(
            search_results.results.exact[x], search_query))

    for x in range(total_approximate):
        if len(msg["embeds"]) == 10:
            break

        msg["embeds"].append(build_vehicle_card(
            search_results.results.approximate[x], search_query))

    for x in range(total_approximateOutside):
        if len(msg["embeds"]) == 10:
            break

        msg["embeds"].append(build_vehicle_card(
            search_results.results.approximateOutside[x], search_query))

    conn = http.client.HTTPSConnection("discord.com")
    payload = json.dumps(msg)
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", api_key, payload, headers)
    res = conn.getresponse()
    print(f'Discord Message Send Status: {res.status} {res.reason}')
    if res.status != 204:
        print("Failed to send message to Discord")
        print(payload)
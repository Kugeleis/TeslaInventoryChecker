import json
import http.client

separator = ", "


def build_vehicle_card(v, zip_code):
    desc = f"→ VIN: {v.VIN}\n"
    desc += f"→ Odometer: {str(v.Odometer)} {v.OdometerType}\n"
    desc += f"→ Price: {str(v.Price)}\n"
    desc += f"→ Sticker Price: {str(v.MonroneyPrice)}\n"
    desc += f"→ Exterior: {separator.join(v.PAINT)}\n"
    desc += f"→ Interior: {separator.join(v.INTERIOR)}\n"
    desc += f"→ Additional Options: {separator.join(v.ADL_OPTS)}\n"
    desc += f"→ Location: {v.City}, {v.StateProvince}"

    card = {
        "title": f"{v.Year} {v.Model.upper()} {v.TrimName} - {separator.join(v.PAINT)}",
        "description": desc,
        "url": f"https://www.tesla.com/{v.Model}/order/{v.VIN}?postal={zip_code}",
        "color": None
    }

    return card


def send_message(api_key, search_query, search_results):
    total_matches = int(search_results.total_matches_found)

    msg = {
        "content": f"{str(total_matches)} {search_query.query.condition} {search_query.query.model.upper()} found within {search_query.query.range} miles of {search_query.query.zip} in {search_query.query.region}",
        "embeds": [
            {
                "title": f"View all {search_query.query.model.upper()} inventory",
                "description": "This link will take you to Tesla's inventory search page.",
                "url": f"https://www.tesla.com/inventory/{search_query.query.condition}/{search_query.query.model}?arrangeby=phl&zip={search_query.query.zip}&range={str(search_query.query.range)}",
                "color": None
            }
        ]
    }

    for x in range(total_matches):
        if x == 9:
            break
        msg["embeds"].append(build_vehicle_card(
            search_results.results[x], search_query.query.zip))

    conn = http.client.HTTPSConnection("discord.com")
    payload = json.dumps(msg)
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", api_key, payload, headers)
    res = conn.getresponse()


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
                "url": f"https://www.tesla.com/inventory/{search_query.query.condition}/{search_query.query.model}?arrangeby=phl&zip={search_query.query.zip}&range={str(search_query.query.range)}",
                "color": None
            }
        ]
    }

    for x in range(total_exact):
        if len(msg["embeds"]) == 10:
            break

        msg["embeds"].append(build_vehicle_card(
            search_results.results.exact[x], search_query.query.zip))

    for x in range(total_approximate):
        if len(msg["embeds"]) == 10:
            break

        msg["embeds"].append(build_vehicle_card(
            search_results.results.approximate[x], search_query.query.zip))

    for x in range(total_approximateOutside):
        if len(msg["embeds"]) == 10:
            break

        msg["embeds"].append(build_vehicle_card(
            search_results.results.approximateOutside[x], search_query.query.zip))

    conn = http.client.HTTPSConnection("discord.com")
    payload = json.dumps(msg)
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", api_key, payload, headers)
    res = conn.getresponse()

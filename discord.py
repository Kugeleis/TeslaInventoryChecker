import json
import http.client


def send_message(api_key, search_query, search_results):
    msg = {
        "content": f"{search_results.total_matches_found} {search_query.query.condition} {search_query.query.model} found within {search_query.query.range} miles of {search_query.query.zip} in {search_query.query.region}",
        "embeds": [
            {
                "title": f"View all {search_query.query.model} inventory",
                "description": "This link will take you to Tesla's inventory search page.",
                "url": f"https://www.tesla.com/inventory/{search_query.query.condition}/{search_query.query.model}?arrangeby=phl&zip={search_query.query.zip}&range={str(search_query.query.range)}",
                "color": None
            }
        ]
    }

    for x in range(int(search_results.total_matches_found)):
        if x == 9:
            break
        v = search_results.results[x]
        separator = ", "
        desc = f"→ VIN: {v.VIN}\n"
        desc += f"→ Odometer: {str(v.Odometer)} {v.OdometerType}\n"
        desc += f"→ Price: {str(v.Price)}\n"
        desc += f"→ Sticker Price: {str(v.MonroneyPrice)}\n"
        desc += f"→ Exterior: {separator.join(v.PAINT)}\n"
        desc += f"→ Interior: {separator.join(v.INTERIOR)}\n"
        desc += f"→ Additional Options: {separator.join(v.ADL_OPTS)}\n"
        desc += f"→ Location: {v.City}"
        msg["embeds"].append({
            "title": f"{v.Year} {v.TrimName} - {separator.join(v.PAINT)}",
            "description": desc,
            "url": f"https://www.tesla.com/{v.Model}/order/{v.VIN}?postal={search_query.query.zip}",
            "color": None
        })

    conn = http.client.HTTPSConnection("discord.com")
    payload = json.dumps(msg)
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", api_key, payload, headers)
    res = conn.getresponse()

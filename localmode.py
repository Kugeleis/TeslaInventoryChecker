import urllib
import helper

def build_vehicle_card(v, search_query):
    desc = "------------------------------------------\n\n"
    desc += f"{v.Year} {v.Model.upper()} {v.TrimName} - {helper.list_to_string(v.PAINT)}\n\n"
    desc += f"→ VIN: {v.VIN}\n"
    try:
        desc += f"→ Odometer: {str(v.Odometer)} {v.OdometerType}\n"
        desc += f"→ Price: {str(v.Price)}\n"
        if v.CountryCode == "US":
            desc += f"→ Sticker Price: {str(v.MonroneyPrice)}\n"
        desc += f"→ Exterior: {helper.list_to_string(v.PAINT)}\n"
        desc += f"→ Interior: {helper.list_to_string(v.INTERIOR)}\n"
        desc += f"→ Additional Options: {helper.list_to_string(v.ADL_OPTS)}\n"
        desc += f"→ Location: {v.City}, {v.StateProvince}, {v.CountryCode}\n"
    except Exception as e:
        print(f'error building description for vehicle - {str(e)}')

    desc += f"\nOrder Link: {get_base_url(search_query.query.market)}/{v.Model}/order/{v.VIN}?postal={urllib.parse.quote(search_query.query.zip)}\n"
    desc += "\n\n------------------------------------------\n\n"
    if v.StateProvince != search_query.query.region:
        print(
            f"Vehicle found does not belong in current State/Region.\n---\n\n{v}\n\n---")
    return desc


def get_base_url(market):
    base_url = "https://www.tesla.com"
    if market == "CA":
        base_url += "/en_CA"
    return base_url

def build_search_url(search_query):
    return f"{get_base_url(search_query.query.market)}/inventory/{search_query.query.condition}/{search_query.query.model}?arrangeby=phl&zip={urllib.parse.quote(search_query.query.zip)}&range={str(search_query.query.range)}"

def send_message(search_query, search_results):
    total_matches = int(search_results.total_matches_found)

    print(f"\n{str(total_matches)} {search_query.query.condition} {search_query.query.model.upper()} found within {search_query.query.range} miles of {search_query.query.zip} in {search_query.query.region}")
    print(f"\nView all {search_query.query.model.upper()} inventory:")
    print(f"{build_search_url(search_query)}\n\n")

    for x in range(total_matches):
        if x == 9:
            break
        try:
            print(build_vehicle_card(search_results.results[x], search_query))
        except Exception as e:
            print(f'Error adding vehicle data to search - {str(e)}')

def send_message_split_results(api_key, search_query, search_results):
    total_exact = len(search_results.results.exact)
    total_approximate = len(search_results.results.approximate)
    total_approximateOutside = len(search_results.results.approximateOutside)
    total_split_matches = total_exact + total_approximate + total_approximateOutside

    print(f"\n{str(total_split_matches)} {search_query.query.condition} {search_query.query.model.upper()} found within {search_query.query.range} miles of {search_query.query.zip} in {search_query.query.region}")
    print(f"\nView all {search_query.query.model.upper()} inventory:")
    print(f"{build_search_url(search_query)}\n\n")

    for x in range(total_exact):
        print(build_vehicle_card(search_results.results.exact[x], search_query))

    for x in range(total_approximate):
        print(build_vehicle_card(search_results.results.approximate[x], search_query))

    for x in range(total_approximateOutside):
        print(build_vehicle_card(search_results.results.approximateOutside[x], search_query))
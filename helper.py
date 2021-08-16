from datetime import datetime, timedelta

separator = ", "

def list_to_string(l):
    if type(l) is not list:
        return ""
    
    try:
        return separator.join(l)
    except Exception as e:
        print(f'Failed to join list - {l}. Error: {str(e)}')
        return ""

def try_parse_date_time(dt, add_hours):
    try:
        datetime_object = datetime.strptime(dt.split('.')[0], '%Y-%m-%dT%H:%M:%S')
        return datetime_object.__add__(timedelta(hours=add_hours)).strftime("%B %d %Y %I:%M %p")
    except Exception as e:
        print(f'failure to convert datetime - {str(e)}')
        return dt
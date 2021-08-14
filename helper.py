separator = ", "

def list_to_string(l):
    if type(l) is not list:
        return ""
    
    try:
        return separator.join(l)
    except Exception as e:
        print(f'Failed to join list - {l}. Error: {str(e)}')
        return ""
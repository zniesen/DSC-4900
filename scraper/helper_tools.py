def convert_to_number(text):
    text = text.lower().replace(' reviews', '').replace('(', '').replace(')', '').replace('Helpful', '').replace('Not', '').replace('<!---->')
    if 'k' in text:
        return int(float(text.replace('k', '')) * 1000)
    elif 'm' in text:
        return int(float(text.replace('m', '')) * 1000000)
    else:
        return int(text)

def get_business_url_and_id(driver, want_id):
    raw_url = driver.current_url
    clean_url = raw_url.split('?')
    if want_id:
        identifier = clean_url[0].replace('https://www.yelp.com/biz/', '')
        return clean_url[0], identifier
    else:
        return clean_url[0]

def no_numbers(text):
    no_digits = []
    for i in text:
        if not i.isdigit():
            no_digits.append(i)
    result = ''.join(no_digits)
    return result

def decode_json(parsed_json):
    result = {}
    for key in parsed_json:
        result[str(key.encode('utf-8'))] = str(parsed_json[key]).encode('utf-8')
    return result

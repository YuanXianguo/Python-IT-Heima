import json


def to_json(data):
    """字符串转为JSON"""
    print(type(data))
    json_data = json.loads(data)
    print(type(json_data))
    print(json_data)
    return json_data


def to_str(data):
    """JSON转为字符串"""
    print(type(data))
    str_data = json.dumps(data)
    print(type(str_data))
    print(str_data)
    return str_data


if __name__ == '__main__':
    str_data = """
    [{
        "name": "Tom",
        "gender": "male"
    }, {
        "name": "Jack",
        "gender": "male"   
    }]
    """

    jd = to_json(str_data)
    print("*"*100)
    to_str(jd)

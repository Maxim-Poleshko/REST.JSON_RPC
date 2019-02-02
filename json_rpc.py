from flask import Flask
from flask import request

import json

app = Flask(__name__)

MEMBERS = {
    'denis': {'age': 25, 'gender': 'male', 'name': 'denis'}
}


def add_member(name, age, gender):  # добавляет в MEMBERS
    response_data = {"jsonrpc": "2.0"}
    MEMBERS[name] = {"age": age, "name": name, "gender": gender}
    response_data["result"] = f"We add your member {MEMBERS[name]}"
    return json.dumps(response_data)


def get_member(name):  # возвращет строку по имени из MEMBERS
    member_name = MEMBERS.get(name)
    response_data = {"jsonrpc": "2.0"}
    if member_name is None:
        response_data["error"] = {"code": -32602, "message": "Invalid params"}
    else:
        response_data["result"] = MEMBERS.get(name)
    return json.dumps(response_data)


def response(result):
    response_data = {"jsonrpc": "2.0"}
    response_data['result'] = result
    return json.dumps(response_data)

def ping(ping_request):
    return response(ping_request)


METHODS = {
    "getMember": get_member,
    "addMember": add_member,
    "ping": ping
}


@app.route('/', methods=['POST'])
def handle():
    data = json.loads(request.data.decode('utf-8'))  # кодировка байтов в utf-8
    method_view = METHODS.get(data.get('method'))  # определяет имя метода
    if not method_view:
        return json.dumps({"error": {"code": -32601, "message": "Method not found"}})
    result = method_view(**data.get("params"))
    return result


@app.route('/ping', methods=['POST'])  # проверка соединения
def ping():
    data = json.loads(request.data.decode('utf-8'))
    method_view = METHODS.get(data.get('method'))
    if not method_view:
        return json.dumps({"error": {"code": -32601, "message": "Method not found"}})
    return response('ping_request')


if __name__ == '__main__':
    set = json.load(open("settings.json", "r"))  # файл с настройками
    app.run(port=set['port'], host=set['host'], debug=set['debug'])

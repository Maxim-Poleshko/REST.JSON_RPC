import requests

ping = {"method": "ping"}


def request(server):
    try:
        print(requests.post(server, json=ping).json())
    except requests.exceptions.ConnectionError:
        return "It's not work"


if __name__ == '__main__':
    link = "http://127.0.0.1:4001/ping"
    print(request(link))

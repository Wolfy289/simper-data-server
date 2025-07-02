from flask import Flask, request
from flask_sock import Sock
from datetime import datetime

app = Flask(__name__)
sock = Sock(app)

connected_clients = set()

@app.route('/')
def index():
    return "<a href='/static/index.html'>text</a><br><a href='/api'>input</a>"

@app.route('/api')
def handle_data():
    data = request.args.get('data')
    name = request.args.get('name')
    data = name + "|" + data
    if data:
        print(f"{name,data}")
        regel = f"\n{nu_time()}|{data}"

        stuur_socket_data(regel)

        return str(data)
    return "<p>?name=...&data=...<p>"

@sock.route('/ws')
def websocket_route(ws):
    print("verbonden")
    connected_clients.add(ws)

    try:
        while True:
            msg = ws.receive()
    finally:
        connected_clients.discard(ws)


def stuur_socket_data(data):
    for client in connected_clients.copy():
        client.send(data.replace("\n", "<br>"))


def nu_time():
    nu = datetime.now()
    return f"{nu.timetuple().tm_yday}:{nu.hour:02}:{nu.minute:02}:{nu.second:02}:{int(nu.microsecond / 10000):02}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

from flask import Flask, request
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__, static_folder='static')
socketio = SocketIO(app)

@app.route('/')
def index():
    return read_data("data.txt").replace("\n", "<br>")

@app.route('/api')
def handle_data():
    data = request.args.get('data')
    if data:
        print(f"Ontvangen data: {data}")
        add_data("data.txt", data)
        return str(data)
    else:
        return "?data=...."

@socketio.on('connect')
def handle_connect():
    print("Client connected")

def read_data(bestand):
    with open(bestand, "r") as f:
        inhoud = f.read()
    return inhoud

def add_data(bestand, data):
    tijd = nu_time()
    regel = "\n" + tijd + '|' + str(data)
    with open(bestand, "a") as f:
        f.write(regel)
    # Zend naar alle websocket clients
    socketio.emit('server_time', regel.replace("\n", "<br>"))

def nu_time():
    nu = datetime.now()
    dagen = nu.timetuple().tm_yday 
    uren = nu.hour
    minuten = nu.minute
    seconden = nu.second
    milliseconden = int(nu.microsecond / 10000)

    return f"{dagen}:{uren:02}:{minuten:02}:{seconden:02}:{milliseconden:02}"

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8000)


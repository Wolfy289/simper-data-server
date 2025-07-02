from flask import Flask, request, send_from_directory
from datetime import datetime

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return read_data("data.txt").replace("\n", "<br>")

@app.route('/api')
def handle_data():
    data = request.args.get('data')
    if data:
        print(f"Ontvangen data: {data}")
        add_data("data.txt",data)
        
        return f"{data}"
    else:
        return "?data=...."


def read_data(bestant):
    with open(bestant, "r") as bestand:
        inhoud = bestand.read()
    return inhoud

def add_data(bestant,data):
    with open(bestant, "a") as bestand:
        bestand.write("\n"+nu_time()+'|'+str(data))

def nu_time():
    nu = datetime.now()
    dagen = nu.timetuple().tm_yday 
    uren = nu.hour
    minuten = nu.minute
    seconden = nu.second
    milliseconden = int(nu.microsecond / 10000)

    tijd_string = f"{dagen}:{uren:02}:{minuten:02}:{seconden:02}:{milliseconden:02}"
    return tijd_string


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

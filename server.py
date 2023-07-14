from flask import Flask,request,jsonify,redirect,url_for,render_template
from flask_cors import CORS
import socket

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = None
CORS(app)

IP = socket.gethostbyname(socket.gethostname())
PORT = 25565

clients = []

@app.route('/connect', methods=['POST'])
def connected():
    data = request.json
    uuid = data.get('uuid')
    xPOS = data.get('x')
    yPOS = data.get('y')
    user = {
        'uuid': uuid,
        'xPOS': xPOS,
        'yPOS': yPOS
    }
    clients.append(user)
    print(f'{uuid} Connected at {xPOS},{yPOS}!')
    return jsonify({'message':f'Connected successfully {uuid}'})

@app.route('/disconnect', methods=['POST'])
def disconnected():
    data = request.json
    uuid = data.get('uuid')
    for client in clients:
        if client["uuid"] == uuid:
            clients.remove(client)
    print(f'{uuid} Disconnected!')
    return jsonify({'message':'Client Disconnected Successfully'})

@app.route('/update_pos', methods=['POST'])
def send_data():
    data = request.json
    uuid = data.get('uuid')
    xPOS = data.get('x')
    yPOS = data.get('y')
    for client in clients:
        if client["uuid"] == uuid:
            client['xPOS'] = xPOS
            client['yPOS'] = yPOS
    return jsonify({'message':f'Position updated successfully for {uuid}'})

@app.route('/get_clients', methods=['GET'])
def get_clients():
    return jsonify(clients)

@app.route('/web_version', methods=['GET'])
def web_version():
    return render_template('taptapir.html')

###############
### TESTING ###
###############

@app.route('/show_clients')
def show_clients():
    return clients

@app.route('/reset_clients')
def reset_clients():
    global clients
    print('Resetting Clients!')
    clients = []
    return redirect(url_for('show_clients'))

app.run(host=IP,port=PORT)
from ursina import *
import requests, json

app = Ursina()
window.borderless = False

serverURL = 'http://192.168.2.151:25565'
#prompt_uuid = input('Enter Username: ')
prompt_uuid = 'ursina'

data = {
    'uuid' : prompt_uuid,
    'x' : 0,
    'y' : 0,
}

#Variables
pringDEBUG = False
disconnected = False
clients = []

class Client(Entity):
    def __init__(self, client):
        super().__init__(self)
        self.model='circle'
        self.color=color.red
        self.scale=.75

        self.client = client
        self.uuid = self.client['uuid']
        self.x = self.client['xPOS']*10
        self.y = self.client['yPOS']*10
        self.nameText = Text(parent=scene,text=self.uuid, x=0, y=self.y-0.05,origin=(0,0))
        #self.name = Text(text=self.uuid,visible=True,x=0, y=self.y-0.05,origin=(0,0))

    def updatePOS(self, x, y):
        self.x = x*10
        self.y = y*10
        self.nameText.x = self.x
        self.nameText.y = self.y- 0.05

def connect():
    request = requests.post(serverURL+'/connect', json=data)
    if pringDEBUG:
        print(f'{request.text}')


def disconnect():
    global disconnected
    request = requests.post(serverURL+'/disconnect', json=data)
    if pringDEBUG:
        print(f'{request.text}')
    disconnected = True
    application.quit()

def update_pos():
    request = requests.post(serverURL+'/update_pos', json=data)
    if pringDEBUG:
        print(f'{request.text}')

def get_clients():
    global clients
    request = requests.get(serverURL+'/get_clients')
    client_list = json.loads(request.text)
    for client in client_list:
        if client["uuid"] == data['uuid']:
            #Removes Self from list
            client_list.remove(client)
        else:
            #If Client isn't Self
            if len(clients) >= 1:
                #If already clients in list
                for old_client in clients:
                    if client["uuid"] == old_client["uuid"]:
                        if client["xPOS"] is None:
                            client["xPOS"] = 0
                        if client["yPOS"] is None:
                            client["yPOS"] = 0
                        old_client['Entity'].updatePOS(client["xPOS"],client["yPOS"])
                        client_list.remove(client)
                    else:
                        client["Entity"] = Client(client)
                        clients.append(client)
            else:
                client["Entity"] = Client(client)
                clients.append(client)

############################
### Start of Ursina Code ###
############################

#Connects to Server
invoke(connect, delay=1)

#Creates Player Entity
self = Entity(model='circle',scale=0.75, color=color.blue,uuid=data['uuid'],x=data['x'],y=data['y'], speed=0.05)

#Sends a Position update to Server
def send_update_pos():
    if not disconnected:
        update_pos()
        invoke(send_update_pos, delay=0.25)
#send_update_pos()

#Sends a get Client Position update to Server
def send_get_clients():
    if not disconnected:
        get_clients()
        invoke(send_get_clients, delay=1)
#send_get_clients()

#Update Function
def update():
    if held_keys['w']:
        self.y += self.speed
        update_pos()
    if held_keys['a']:
        self.x -= self.speed
        update_pos()
    if held_keys['s']:
        self.y -= self.speed
        update_pos()
    if held_keys['d']:
        self.x += self.speed
        update_pos()
    data['x'] = round(self.x, 2)
    data['y'] = round(self.y, 2)
    get_clients()

#Keyboard Function
def input(key):
    if key == 'g':
        get_clients()
    if key == 'f':
        print(clients)
    if key == 'q':
        disconnect()


app.run()
disconnect()
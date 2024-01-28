import socket
import threading
import json
import sqlite3
import time

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ADRESSE = ('127.0.0.1',12345)
s.bind(ADRESSE)
s.listen()
print("SERVER LISTENING.....")
clients = []
names = []
rooms = {}
blocked_users ={}
#DataBase++++++++++++++++++++++++++++++++++++++++++++++++
def all_users():
    conn = sqlite3.connect("DATA.db")
    c = conn.cursor()
    c.execute("SELECT Username FROM CLIENT")
    record = c.fetchall()
    conn.commit()
    conn.close()
    return record

def add_to_database(info):
    conn = sqlite3.connect("DATA.db")
    c = conn.cursor()
    c.execute("SELECT Username FROM CLIENT WHERE Username = ?", (info['Username'],))
    existing_user = c.fetchone()
    if existing_user:
        client.send("exist".encode('utf-8'))
    else:
        c.execute("INSERT INTO CLIENT VALUES(:Username,:First,:Last,:Phone,:Password)",
        {
            'Username' : info['Username'],
            'First' : info['first_name'],
            'Last' : info['last_name'],
            'Phone' : info['phone'],
            'Password' : info['password']})
        client.send("done".encode('utf-8'))
    conn.commit()
    conn.close()

def verify_client(login):
    conn = sqlite3.connect("DATA.db")
    c = conn.cursor()
    c.execute("SELECT * FROM CLIENT WHERE Username = ? AND Password = ?", (login['Username'], login['password']))
    record = c.fetchone()
    conn.close()
    return record is not None

def historique_room(name):
    conn = sqlite3.connect("DATA.db")
    c = conn.cursor()
    c.execute("SELECT sender,message FROM ROOM WHERE name_room = ?",(name,))
    record = c.fetchall()     
    conn.commit()
    conn.close()
    return record

def historique_prv(sender,receiver):
    conn = sqlite3.connect("DATA.db")
    c = conn.cursor()
    c.execute("SELECT sender,message,receiver FROM PRIVE WHERE (sender =? and receiver = ?) or (sender =? and receiver = ?)",(sender,receiver,receiver,sender))
    record = c.fetchall()
    conn.commit()
    conn.close()
    return record

def all_rooms():
    conn = sqlite3.connect("DATA.db")
    c = conn.cursor()
    c.execute("SELECT DISTINCT name_room FROM ROOM")
    record = c.fetchall()
    conn.commit()
    conn.close()
    return record 

def room_database(info):
    conn = sqlite3.connect("DATA.db")
    c = conn.cursor()
    c.execute("INSERT INTO ROOM VALUES(:name_room,:sender,:message)",
    {
        'name_room' : info['name_room'],
        'sender' : info['sender'],
        'message': info['message'],
    })
    conn.commit()
    conn.close()

def prive_database(info):
    conn = sqlite3.connect("DATA.db")
    c = conn.cursor()
    c.execute("INSERT INTO PRIVE VALUES(:sender,:receiver,:message)",
    {
        'sender' : info['sender'],
        'receiver' : info['receiver'],
        'message': info['message'],
    })
    conn.commit()
    conn.close()

def change_name(old_name,new_name):
    conn = sqlite3.connect("DATA.db")
    c = conn.cursor()
    c.execute("SELECT Username FROM CLIENT WHERE Username = ?", (new_name,))
    existing_user = c.fetchone()
    if existing_user:
        client.send("rep,exist".encode('utf-8'))
    else:
        c.execute("UPDATE CLIENT SET Username = ? WHERE Username = ?",(new_name,old_name))
        if c.rowcount > 0:
            for name in names:
                if name == old_name:
                    names[names.index(name)] = new_name
            c.execute("UPDATE PRIVE SET sender = ? WHERE sender = ?",(new_name,old_name))
            c.execute("UPDATE PRIVE SET receiver = ? WHERE receiver = ?",(new_name,old_name))
            c.execute("UPDATE ROOM SET sender = ? WHERE sender = ?",(new_name,old_name))
            client.send("rep,done".encode('utf-8'))
    conn.commit()
    conn.close()
    

#DataBase++++++++++++++++++++++++++++++++++++++++++++++++

def get_name(client):
    if client in clients:
        index=clients.index(client)
        name= names[index]
        return name

def get_socket(name):
    index = names.index(name)
    client = clients[index]
    if client in clients:
        return client

def get_room(client):
    for room, clients in rooms.items():
        if client in clients:
            return room

def broadcast_room(message, client):
    global room_name
    name_sender = get_name(client)
    msg = message.decode()
    if ":" in msg:
        msg = msg.split(',')[0]
        msg = msg.split(":")[1]
    for c in rooms.get(room_name,[]):
        if c != client:
            try:
                c.send(message)
                if "room" not in msg:
                    data_room = {
                        'name_room':room_name,
                        'sender' : name_sender,
                        'message' : msg,}
                    room_database(data_room)
            except:
                c.close()
                if c in rooms[room_name]:
                    rooms[room_name].remove(c)

def liste_connection(client):
    client.send("enlign".encode("utf-8"))
    name = get_name(client)
    info = list(names)
    if name in info:
        info.remove(name)
    login = json.dumps(info)
    time.sleep(0.1)
    client.send(login.encode("utf-8"))

def liste_users(client):
    client.send("us".encode("utf-8"))
    users = all_users()
    for enlign in names:
        for nam in users:
            if enlign == nam[0]:
                users.remove(nam)
                break
    users = json.dumps(users)
    client.send(users.encode("utf-8"))

def liste_rooms(client):
    client.send("R".encode('utf-8'))
    list_roomdb = all_rooms()
    liste_rooms = list(rooms.keys())
    for room in list_roomdb:
        if room[0] not in liste_rooms:
            liste_rooms.append(room[0])
            if room[0] not in rooms:
                rooms[room[0]] = [] 
    inf = json.dumps(liste_rooms)
    client.send(inf.encode('utf-8'))

def broadcast(message):
    for client in clients:
        client.send(message)

def blockuser(sender, receiver):
    if receiver in blocked_users:
        blocked_users[receiver].append(sender)
    else:
        blocked_users[receiver] = [sender]
    sender_client = get_socket(sender)
    if sender_client:
        sender_client.send(f"You blocked {receiver}.Unable to send the message".encode('utf-8'))

def debloquer(sender,receiver):
    if receiver in blocked_users and sender in blocked_users[receiver]:
        blocked_users[receiver].remove(sender)
    sender_client = get_socket(sender)
    if sender_client:
        sender_client.send(f"You unblocked {receiver}.".encode('utf-8'))
    else:
        if sender_client:
            sender_client.send(f"{receiver} is not blocked.".encode('utf-8'))
            

def handle(client):
    global room_name
    name = None
    while True:    
        try:
            msg = client.recv(1024).decode()
            if msg == "signup":
                info_string = client.recv(1024).decode()
                info = json.loads(info_string)
                add_to_database(info)

            elif msg == "connect":
                stored_json = client.recv(1024).decode()
                login = json.loads(stored_json)
                verification = verify_client(login)
                if verification:
                    client.send("Correct".encode("utf-8"))
                    name = client.recv(1024).decode()
                    names.append(name)
                    client.send(f"{name} CONNECTED TO SERVER!\n-join room \n-create your room\n-send private message".encode('utf-8'))
                else:
                    client.send("False".encode("utf-8"))
            
            elif msg == "users":
                for client in clients:
                    liste_connection(client)
                    time.sleep(0.1)
                    liste_users(client)
                    time.sleep(0.2)
                    liste_rooms(client)
                    
            elif "room" in msg:
                room_name = msg.split(',', 1)[1]
                client.send("newroom".encode('utf-8'))
                if room_name not in rooms:
                    rooms[room_name] = []
                    client.send(f"you created a room <{room_name}>".encode('utf-8'))
                else:
                    client.send(f"room exist!".encode('utf-8'))
            
            elif "historique" in msg:
                message = msg.split(",")
                name_reciver = message[1]
                cli_reciver = get_socket(name_reciver)
                name_sender = get_name(client)
                record = historique_prv(name_sender,name_reciver)
                client.send(f"historique_prv".encode('utf-8'))
                histo = json.dumps(record)
                time.sleep(0.1)
                client.send(histo.encode("utf-8"))
                
            elif "prv" in msg:
                message = msg.split(",")    
                name_receiver = message[1]
                cli_reciver = get_socket(name_reciver)
                name_sender = get_name(client) 
                msg1 = message[2]
                if name_sender in blocked_users and name_receiver in blocked_users[name_sender]:
                    client.send(f"You are blocked by {name_receiver}. Unable to send the message.".encode("utf-8"))
                else:
                    cli_reciver.send(f'{name_sender}:{msg1}:PRV'.encode("utf-8"))
                    time.sleep(0.1)
                    cli_reciver.send(f'{name_sender}:{msg1}'.encode("utf-8")) 
                    info ={
                        'sender' : name_sender,
                        'receiver' : name_reciver,
                        'message' : msg1
                    }
                    prive_database(info)
                    
            elif "ROOMNAME" in msg:
                try:
                    room_name = msg.split(',', 1)[1]
                    if client not in rooms[room_name]:
                        rooms[room_name].append(client)
                        client.send(f"you are join room <{room_name}>".encode('utf-8'))
                        time.sleep(0.1)
                        broadcast_room(f'{name} joined room <{room_name}>'.encode('utf-8'), client)
                    record = historique_room(room_name)
                    client.send("historique_room".encode("utf-8"))
                    histo = json.dumps(record)
                    client.send(histo.encode("utf-8"))
                except:
                    print("erreur")
            
            elif "change" in msg:
                msg = msg.split(',')
                old_name = msg[1]
                new_name = msg[2]
                name=new_name
                change_name(old_name,new_name)

            elif msg =="mise":    
                liste_connection(client)
                time.sleep(0.1)
                liste_users(client)
                time.sleep(0.1)
                liste_rooms(client)
            
            elif "bloquer" in msg:
                name_sender=msg.split(',')[1]
                name_receiver=msg.split(',')[2]
                blockuser(name_sender,name_receiver)
            
            elif "déb" in msg:
                name_sender=msg.split(',')[1]
                name_receiver=msg.split(',')[2]
                debloquer(name_sender,name_receiver)
            
            else:
                room = msg.split(',')[1]
                for room_name in list(rooms.keys()):
                    if room == room_name:
                        broadcast_room(f'{name} : {msg},room'.encode('utf-8'), client)
        except: 
            name = get_name(client)           
            if client in clients:
                clients.remove(client) 
            broadcast(f'{name} left the chat'.encode("utf-8"))   
            if name in names:
                names.remove(name)        
            client.close()
            break
while True:
    client,adrr = s.accept()
    print(f"CONNECTED WITH {adrr}!")
    clients.append(client)
    thread = threading.Thread(target=handle,args=(client,))
    thread.start()  
    
        
    
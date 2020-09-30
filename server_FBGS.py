import tkinter as tk
from tkinter import ttk
import os
import tkinter as tk
import threading
import time
import Toma_muestra
import matplotlib.pyplot as plt
import hyperion
import pickle
import numpy as np
import socket
from matplotlib.animation import FuncAnimation

SERVER = '192.168.43.230'
PORT = 5050
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECT!'
print('IP del servidor:'+SERVER)
ADDR = (SERVER,PORT)
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)
def orden_comienzo():
    try:
        msg_lenght = int(client.recv(HEADER).decode(FORMAT))
    except:
        continue
    msg =client.recv(msg_lenght).decode(FORMAT)
    print(msg)
    if msg == 'Comienzo':
       return True
comienzo = False


while not comienzo:
    comienzo = orden_comienzo()


h1 = hyperion.Hyperion('10.0.0.55')


def envio_canales(h1,client):
    numero_sensores ={1:'',2:'',3:'',4:''}
    canales =[]
    for canal in range(1,5):
            try:
                    peaks = self.h1.peaks[canal]
                    print(f"picos canal {canal}:{peaks}")
                    if len(peaks)>0:
                            canales.append(canal)
                            numero_sensores[canal]=len(peaks)
            except:
                    print(f"canal {canal} sin sensores")
    client.send('Canales')
    msg_length = len(canales)
    send_length = str(msg_length).encode(FORMAT)
    send_length  += b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.sendall(pickle.dumps((canales,numero_sensores)))
    return (canales,numero_sensores)
    
(canales,numero_sensores)=envio_canales(h1,client)
#t_0= time.time()
#t_anterior =0
#self.Temperaturas={1:[],2:[],3:[],4:[]}



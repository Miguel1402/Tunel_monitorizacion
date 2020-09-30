#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  client.py
#  
#  Copyright 2020 Miguel <Miguel@DESKTOP-ELM50LG>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import socket
from PIL import Image
import matplotlib.pyplot as plt
import pickle
PORT = 5050
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECT!'
print('leyendo imagen')
im = Image.open('IMG.jpg')

pixels =im.tobytes()
print('Guardandola en diccionario')
Imagen = {'pixels':pixels,
            'size':im.size,
            'mode':im.mode}
print('codificando')
elemento_imagen = pickle.dumps(Imagen)
#elemento_2 = pickle.loads(elemento_imagen)
#Imagen_2 = Image.new(Imagen['mode'],Imagen['size'])
#Imagen_2.putdata(Imagen['pixels'])
#print(2)
#plt.imshow(Imagen_2)
#print(1)
#plt.show()
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = '192.168.43.230'
print('IP del servidor:'+SERVER)
ADDR = (SERVER,PORT)
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length  += b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)


def send_Image(imagen):
    msg = 'Imagen'
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    msg_length = len(imagen)
    send_length = str(msg_length).encode(FORMAT)
    send_length  += b' '*(HEADER-len(send_length))
    print(send_length)
    client.send(send_length)
    client.sendall(imagen)
    



send_Image(elemento_imagen)
send(DISCONNECT_MESSAGE)





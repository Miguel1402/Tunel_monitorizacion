import socket 
import pickle
import time
import threading
import PIL
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import io
from ventanas_emergentes import Ventana_Apertura,Ventana_principal
PORT = 5050
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECT!'
SERVER ='130.206.92.100'

#SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER,PORT)


Datos_iniciales = Ventana_Apertura()

Base_sensores = pd.read_csv(f'calibraciones//{Datos_iniciales.perfil}',sep=';')
Base_sensores.index = Base_sensores.nombre_fibra
print(Base_sensores)
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def send(conn,msg):
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length  += b' '*(HEADER-len(send_length))
	conn.send(send_length)
	conn.send(message)

server.bind(ADDR)

def handle_client(conn,addr):
	print(f"[NEW CONNECTION] {addr} connected")
	connected= True
	while connected:
		try:
			msg_lenght = int(conn.recv(HEADER).decode(FORMAT))
		except:
			continue
		msg =conn.recv(msg_lenght).decode(FORMAT)
		print(msg)
		
		if msg == DISCONNECT_MESSAGE:
			connect=False
		if msg == 'Muestra': 
			try:
				print('leyendo header')
				msg_lenght = int(conn.recv(HEADER).decode(FORMAT))
				
			except:
				pass 
			print(msg_lenght)
			msg=b''
			while len(msg)<msg_lenght:
				msg =msg+conn.recv(msg_lenght)
			
			print(len(msg))
			#print(list(msg))
			
			Muestra = pickle.loads(msg)
			print(f'El mensaje recibido es un {type(Muestra)}')
			#Imagen_2 = Image.frombytes(Imagen['mode'],Imagen['size'],Imagen['pixels'])
			print(Muestra)
			#plt.imshow(Imagen_2)
			#plt.show()
			
		if msg == 'Canales': 
			try:
				print('leyendo header')
				msg_lenght = int(conn.recv(HEADER).decode(FORMAT))
			except:
				pass 
			print(msg_lenght)
			msg=b''
			while len(msg)<msg_lenght:
				msg =msg+conn.recv(msg_lenght)
			print(len(msg))
			(canales,numero_sensores) = pickle.loads(msg)
			print(f'El mensaje recibido es un {type((canales,numero_sensores))}')
			print((canales,numero_sensores))
			Datos_ensayo=Ventana_principal(Base_sensores,numero_sensores,conn,canales,HEADER,FORMAT)
			print('Guardando en:'+Datos_ensayo.carpeta_guardado)
			connected=False	
			from Guardado_objeto import guardado_objeto
			guardado_objeto(Datos_ensayo.carpeta_guardado,Datos_ensayo,Datos_iniciales)

	conn.close()	
		
		


def start():
	server.listen()
	while True:
		#waits until a new connection	
		conn,addr =server.accept()
		time.sleep(1)
		send(conn,'Comienzo')
		thread = threading.Thread(target = handle_client,args=(conn,addr))
		thread.start()
		
		
start()

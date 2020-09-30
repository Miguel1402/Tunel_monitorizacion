import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
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
class Ventana_Apertura():
    def __init__(self):
        
        self.window = tk.Tk()
        self.window.geometry('500x500')

        self.compo=ttk.Combobox()
        self.compo.grid(row=2,column=1)
        self.compo['values']= os.listdir('calibraciones')

        tk.Label(self.window,text='LWC (g/m3)').grid(row=0)
        tk.Label(self.window,text='MVD (um)').grid(row=1)
        tk.Label(self.window,text='Perfil').grid(row=2)
        self.e1=tk.Entry(self.window)
        self.e2=tk.Entry(self.window)
        self.e1.grid(row=0,column=1)
        self.e2.grid(row=1,column=1)

        B = tk.Button(self.window,text='Guardar',command=self.guardar_comanda)
            
        B.grid(row=3)
        self.window.mainloop()
        
    def guardar_comanda(self):
        
        self.MVD = str(self.e2.get())
        self.LWC =str(self.e1.get())
        self.perfil=self.compo.get()



class Ventana_principal(object):
    def __init__(self,Base_sensores,numero_sensores,conn,canales,HEADER,FORMAT):
        self.conn = conn
        self.HEADER=HEADER
        self.FORMAT = FORMAT
        self.canales = canales
        self.comienzo = True
        self.Base_sensores=Base_sensores
        self.numero_sensores = numero_sensores
        self.canales = canales
        t_0= time.time()
        self.t_0 = t_0
        self.Temperaturas={1:[],2:[],3:[],4:[]}
        Hilo_ventana_control = threading.Thread(target=self.ventana_control).start()
        self.DISCONNECT_MESSAGE = 'DISCONNECT!'
        self.connected=True
        while self.connected:
            for canal in canales:
                Muestra=[]
                muestra = list(self.receive_sample(canal))
                constantes_sensor = Base_sensores[Base_sensores.canal==canal]
                for sensor in range(len(muestra)):
                    constantes_sensor = Base_sensores[Base_sensores.canal==canal].loc['FBG'+str(sensor+1)]
                    fbg = muestra[sensor]
                    Muestra.append(constantes_sensor['A']*fbg**3+constantes_sensor['B']*fbg**2+
                                    constantes_sensor['C']*fbg+constantes_sensor['D'])
                
                t_anterior =time.time()-t_0
                Muestra.append(time.time()-t_0)

                self.Temperaturas[canal].append(Muestra)
            time.sleep(1)

        ventana =tk.Tk()
        ventana.carpeta = filedialog.askdirectory(initialdir='/media/pi/KINGSTON')   
        self.carpeta_guardado = ventana.carpeta
    def ventana_control(self): 
        self.Ventana = tk.Tk()
        self.listbox = tk.Listbox(self.Ventana )
        self.listbox.grid(row=0)
        botones = []

        for canal in self.canales:
            self.canal = canal
             #lambda s=item: func(s)
            botones.append(tk.Button(self.Ventana, text=f"canal {canal}", command=lambda i =canal: self.callback(i)))
            botones[-1].grid(row=0,column=canal+1)
        boton_desconectar = tk.Button(self.Ventana, text='Desconectar', command=self.desconexion)
        boton_desconectar.grid(row=1)
        tk.mainloop()
    def callback(self,canal):
        Hilo = threading.Thread(target=self.ventana_canal,args=(canal,))
        Hilo.start()
                
    def ventana_canal(self,canal):
        Numero_sensores = self.numero_sensores[canal]
        
        #Sale una ventana emergente con Toplevel
        Ventana= tk.Toplevel()
        #En nombre de la ventana es canal
        Ventana.wm_title(f"Canal {canal}")
        botones = []
       
        for sensor in range(Numero_sensores):
            botones.append(tk.Button(Ventana, text=f"sensor {sensor+1}", command=lambda j =sensor+1: self.callback_sensor(j,canal)))
            botones[-1].grid(row=sensor)
        
    def callback_sensor(self,sensor,channel):
        fig,ax = plt.subplots()
        def funcion_animacion(i):
            ax.clear()
            ax.plot(np.array(self.Temperaturas[channel])[:,-1],np.array(self.Temperaturas[channel])[:,sensor-1])
            ax.set_xlabel('t(s)')
            ax.set_ylabel('T(ºC)')
            ax.set_title(f'Sensor {sensor} Canal {channel}')
            
            
        self.listbox.insert(tk.END, "sensor"+str(sensor)+"canal"+str(channel))
        anim = FuncAnimation(fig,funcion_animacion,interval =1000)
        plt.show()
        
    def send(self,msg):
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length  += b' '*(self.HEADER-len(send_length))
        self.conn.send(send_length)
        self.conn.sendall(msg.encode(self.FORMAT))
        
    def receive_sample(self,channel):
        self.send('Muestra')
        
        envio_sensor_muestra = pickle.dumps(channel)
        msg_length = len(envio_sensor_muestra)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length  += b' '*(self.HEADER-len(send_length))
        self.conn.send(send_length)
        self.conn.sendall(envio_sensor_muestra)
        msg_lenght = int(self.conn.recv(self.HEADER).decode(self.FORMAT))

        msg =self.conn.recv(msg_lenght)
        
        return pickle.loads(msg)

    def desconexion(self):
        self.connected= False
        

  
        
       

            


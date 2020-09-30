#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  aplicacion.py
#  
#  Copyright 2020  <pi@raspberrypi>
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


import ventanas_emergentes
import pandas as pd
import Toma_muestra
import time

Datos_entrada=ventanas_emergentes.Ventana_Apertura()
Base_sensores = pd.read_csv(f'calibraciones//{Datos_entrada.perfil}',sep=';')
Base_sensores.index = Base_sensores.nombre_fibra
Temperaturas_ensayo=[]
T=[]
canales =[]
for canal in range(1,5):
        try:
                peaks = h1.peaks[canal]
                print(f"picos canal {canal}:{peaks}")
                if len(peaks)>0:
                        canales.append(canal)
        except:
                print(f"canal {canal} sin sensores")

Programa_principal = ventanas_emergentes.Ventana_principal(Base_sensores)        

    


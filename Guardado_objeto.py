from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import os
import subprocess
def guardado_pdf(carpeta):
    condiciones = pd.read_csv(carpeta+'//condiciones.txt')
    directorio_principal =os.getcwd()
    escudo_inta=directorio_principal.replace('\\','/')+'/logo-inta.png'
    figura_fbg =carpeta.replace('\\','/')+'/Figure_1.png'
    file = open(carpeta+'//main.tex','w')
    file.write(r'\documentclass[12pt]{article}'+'\n')
    file.write(r'\usepackage{graphicx}'+'\n')
    file.write(r'\begin{document}'+'\n')
    file.write(r'\begin{figure}[h!]'+'\n')
    file.write(r'\centering'+'\n')
    file.write(r'\includegraphics[width=3cm]{'+escudo_inta+'}'+'\n')
        
    file.write(r'\end{figure}'+'\n')
    file.write(r'\section{FBGS}'+'\n')
    file.write(r'\begin{figure}[h!]'+'\n')
    file.write(r'\centering'+'\n')
    file.write(r'\includegraphics[width=3cm]{'+figura_fbg+'}'+'\n')
    file.write(r'\end{figure}'+'\n')
    file.write(r'\section{Condiciones}'+'\n')
    for i in condiciones.index:
        file.write(condiciones['condicion'].loc[i]+':\t'+str(condiciones['valor'].loc[i])+'\n')
    file.write(r'\end{document}'+'\n')
    file.close()
    df = pd.read_csv(carpeta+'//FBGS.txt')
    df.index = df['Time(s)']
    del df['Time(s)']
    df.plot()
    plt.savefig(carpeta+'//Figure_1.png')

    plt.show()
    archivo_latex = str(carpeta+'//main.tex')
    archivo_latex= archivo_latex.replace('//','/')
    subprocess.run(['pdflatex',archivo_latex])




def guardado_objeto(carpeta,datos,datos_iniciales):
    file = open(carpeta+'//FBGS.txt','w')
    tiempo = datetime.fromtimestamp(datos.t_0)
    for canal in datos.canales:
        for sensor in range(1,len(datos.Temperaturas[canal][0])):
            file.write('FBG'+str(canal)+'_'+str(sensor)+',')
    file.write('Time(s)')
    file.write('\n')
    n_muestras= len(datos.Temperaturas[datos.canales[0]])
    for muestra in range(n_muestras):
        for canal in datos.canales:
            for sensor in range(len(datos.Temperaturas[canal][0])-1):
                
                file.write(str(datos.Temperaturas[canal][muestra][sensor])+',')
        file.write(str(datos.Temperaturas[canal][muestra][-1]))
        file.write('\n')
    file.close()
    file = open(carpeta+'//condiciones.txt','w')
    file.write('condicion,valor\n')
    file.write('Tiempo inicio del ensayo,'+str(tiempo)+'\n')
    file.write('LWC (g/m3),'+datos_iniciales.LWC+'\n')
    file.write('MVD (um),'+datos_iniciales.MVD+'\n')
    file.close()
    guardado_pdf(carpeta)
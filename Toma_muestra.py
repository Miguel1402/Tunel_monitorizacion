import time
def Toma_muestras(channel,Base_sensores,t_0,h1):
    peaks = h1.peaks[channel]
    T=[]
    for j in range(len(peaks)): 
        constantes_sensor = Base_sensores.loc['FBG'+str(j+1)]
        fbg = peaks[j]
        T.append(constantes_sensor['A']*fbg**3+constantes_sensor['B']*fbg**2+constantes_sensor['C']*fbg+constantes_sensor['D'])
        
    t=time.time()-t_0
    T.append(round(t,1))
    return T

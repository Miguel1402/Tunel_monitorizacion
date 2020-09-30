import hyperion
def canales_activos():
    h1 = hyperion.Hyperion('10.0.0.55')
    canales =[]
    for canal in range(1,5):
            try:
                    peaks = h1.peaks[canal]
                    print(f"picos canal {canal}:{peaks}")
                    if len(peaks)>0:
                            self.canales.append(canal)
                            self.numero_sensores[canal]=len(peaks)
            except:
                    print(f"canal {canal} sin sensores")
    return canales

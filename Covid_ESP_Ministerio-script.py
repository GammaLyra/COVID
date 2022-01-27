import pandas as pd
import numpy as np
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import matplotlib.dates as mdates
from statsmodels.tsa.seasonal import seasonal_decompose

#----------------------------------------------------------------------------
# FUNCIONES
#----------------------------------------------------------------------------

# función para distribuir los datos entre los valores NULL 
def redistribute_nan (df, columns=[]):
    l = len(df)
    for c in columns:
        print ("redistributing column " + c + "..." + "(" + str(sum(np.isnan(df[c]))) + ")")
        for i in range(l-1,0,-1): # Ignora la primera fila ya que siempre es NULL
            # Busca los valores negativos
            if np.isnan(df.iloc[i][c]):
                n = 1
                # Calcula el número consecutivo de NULL values
                while (np.isnan(df.iloc[i-n][c])):
                    n += 1
                # hacemos la distribución de los valores entre los NULL
                value = df.iloc[i+1][c]
                value_r = int(value/(n+2)) # instead of n+1 to double the weight of current day
                df.at[df.index[i+1],c] = df.iloc[i+1][c] - value_r * n
                for j in range(n):
                    df.at[df.index[i-j],c] = value_r
    # Comprobamos que no quedan NULL sin corregir (solo el primer valor)            
    for c in columns:
        print ("after redistributing column " + c + "..." + "(" + str(sum(np.isnan(df[c]))) + ")")
    print ('')
    df_red = df
    return df_red

# función para corregir los valores negativos
def redistribute_negatives (df, columns=[], ndays = 30):
    l = len(df)
    for c in columns:
        print ("redistributing column " + c + "..." + "(" + str(sum(df[c]<0)) + ")")
        for i in range(l-1,0,-1): # ignore first row as it is known to be missing
            # look for negative values
            if df.iloc[i][c] < 0:
                value = df.iloc[i][c]
                first = max(0,i-ndays)
                prev = df.iloc[first:i][c]
                lprev = sum(~np.isnan(prev))
                value_r = np.floor (value / lprev)
#                     print (i, first, value, value_r, prev.min())
                for j in range(i-1,first-1,-1):
                    df.iloc[j][c] = df.iloc[j][c] + value_r
                df.iloc[i][c] = value - value_r * lprev
                        
    for c in columns:
        print ("after redistributing column " + c + "..." + "(" + str(sum(df[c]<0)) + ")")
    print ('')
    df_red = df
    return df_red
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------


# Leemos los datos del fichero csv
file_path="tablas_ini/COVID_ESP_Ministerio.csv"
data=pd.read_csv(file_path,converters={"fecha":pd.to_datetime})

# Cambiamos la fecha a dateframe
data['fecha'] = pd.to_datetime(data["fecha"].dt.strftime('%d-%m-%Y'))

# Calculamos los datos diarios como la diferencia de los totales
data['casos_24h']=data["casos_tot"].diff()
data['fallecidos_24h']=data["fallecidos_tot"].diff()

# Ponemos la fecha como indice, añadimos los días que faltan
data=data.set_index("fecha")
data=data.resample("D").asfreq()

# Redistribuimos los datos para que no haya NULL values
cols_red = ['casos_24h','fallecidos_24h']

data_temp = data.copy()
csum, fsum = data_temp[cols_red].sum()

print ("** REDISTRIBUTE MISSING VALUES **")
data_red = redistribute_nan (data_temp,columns=cols_red)
csum_red, fsum_red = data_red[cols_red].sum()

print ("** TOTAL SUM **")
print("before", int(csum), int(fsum))
print("after", int(csum_red), int(fsum_red), '\n')

print ("** REDISTRIBUTE NEGATIVE VALUES **")
data_red2 = redistribute_negatives (data_red,columns=cols_red,ndays=30)
csum_red2, fsum_red2 = data_red2[cols_red].sum()

print ("** TOTAL SUM **")
print("before", int(csum), int(fsum))
print("after", int(csum_red2), int(fsum_red2), '\n')

# Calculamos la indicencia a 14 dias
data_red2=data_red2.reset_index()
IA_14d=[None]*13

for i in data_red2.index[13:]:
    if (not np.isnan(data_red2["casos_24h"].iloc[i])):
        IA_14d.append("{:.2f}".format(data_red2["casos_24h"].iloc[i+1-14:i+1].sum()*1e5/47351567))
    else:
        IA_14d.append(None)

IA_14d=np.array(IA_14d,dtype=float)

data_red2["IA_14d"]=IA_14d


# Calculamos la indicencia a 7 dias
IA_7d=[None]*6

for i in data_red2.index[6:]:
    if (not np.isnan(data_red2["casos_24h"].iloc[i])):
        IA_7d.append("{:.2f}".format(data_red2["casos_24h"].iloc[i+1-7:i+1].sum()*1e5/47351567))
    else:
        IA_7d.append(None)

IA_7d=np.array(IA_7d,dtype=float)

data_red2["IA_7d"]=IA_7d


# Ponemos la fecha como indice
data_red2=data_red2.set_index("fecha")


# Sumamos los datos semanalmente
data_sem=data_red2.resample('W').sum()
data_sem.drop("casos_tot",axis=1,inplace=True)
data_sem.drop("fallecidos_tot",axis=1,inplace=True)
data_sem.drop("IA_14d",axis=1,inplace=True)
data_sem.drop("IA_7d",axis=1,inplace=True)

# Guardamos los datos que acabamos de calcular en tablas .csv

# Datos de casos cada 24h, fallecidos cada 24h, IA 14d y IA 7d con todos los datos, incluidos los NULL
data_temp3=data_red2[["casos_tot","fallecidos_tot","casos_24h","fallecidos_24h","IA_14d","IA_7d"]].copy()
data_temp3.to_csv(path_or_buf="tablas_temp/datos_ESP.csv")

# Datos de hospitalizaciones y UCIS
data_temp=data[["UCI","hospitalizados"]].copy()
data_temp=data_temp.dropna()
data_temp.to_csv(path_or_buf="tablas_temp/datos_ESP_hosp_UCI.csv")

# Datos de casos y fallecidos semanales
data_sem[["casos_24h","fallecidos_24h"]].to_csv(path_or_buf="tablas_temp/datos_ESP_sem.csv")

print("------ Datos de España del Ministerio terminado --------")


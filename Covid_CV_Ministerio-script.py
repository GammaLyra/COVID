import pandas as pd
import numpy as np
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import matplotlib.dates as mdates
from statsmodels.tsa.seasonal import seasonal_decompose


# Leemos los datos del fichero csv
file_path="tablas_ini/COVID_CV_Ministerio.csv"
data=pd.read_csv(file_path,converters={"fecha":pd.to_datetime})

# Cambiamos el formato de la columna UCI a float y de la fecha a dateframe
data["UCI"] = pd.to_numeric(data.UCI, errors='coerce')
data['fecha'] = pd.to_datetime(data["fecha"].dt.strftime('%d-%m-%Y'))

# Calculamos los datos diarios como la diferencia de los totales
data['casos_24h']=data["casos_tot"].diff()
data['fallecidos_24h']=data["fallecidos_tot"].diff()

# Ponemos la fecha como indice, añadimos los días que faltan y volvemos a quitar la fecha como indice
data=data.set_index("fecha")
data=data.resample("D").asfreq()
data=data.reset_index()


# Calculamos la indicencia a 14 dias

IA_14d=[None]*13

for i in data.index[13:]:
    if (not np.isnan(data["casos_24h"].iloc[i])):
        IA_14d.append("{:.2f}".format(data["casos_24h"].iloc[i+1-14:i+1].sum()*1e5/5057353))
    else:
        IA_14d.append(None)

IA_14d=np.array(IA_14d,dtype=float)

data["IA_14d_me"]=IA_14d


# Calculamos la indicencia a 7 dias
IA_7d=[None]*6

for i in data.index[6:]:
    if (not np.isnan(data["casos_24h"].iloc[i])):
#         IA_7d.append("{:.2f}".format(data["casos_24h"].iloc[i+1-7:i+1].sum()*1e5/4.975e6))
        IA_7d.append("{:.2f}".format(data["casos_24h"].iloc[i+1-7:i+1].sum()*1e5/5057353))
    else:
        IA_7d.append(None)

IA_7d=np.array(IA_7d,dtype=float)

data["IA_7d_me"]=IA_7d

# Volvemos a poner la fecha como indice
data=data.set_index("fecha")

# Guardamos en una tabla los datos que nos interesa: UCIs y hospitalizaciones
data_temp=data[["UCI","hospitalizados"]].copy()
data_temp=data_temp.dropna()
data_temp.to_csv(path_or_buf="tablas_temp/datos_CV_hosp_UCI.csv")




print("------ Datos de la C. Valenciana del Ministerio terminado --------")

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import matplotlib.dates as mdates
from statsmodels.tsa.seasonal import seasonal_decompose


# In[2]:


# Leemos los datos del fichero csv
file_path="COVID_ESP_Ministerio.csv"
data=pd.read_csv(file_path,converters={"fecha":pd.to_datetime})

# Cambiamos el formato de la columna UCI a float y de la fecha a dateframe
# data["UCI"] = pd.to_numeric(data.UCI, errors='coerce')
data['fecha'] = pd.to_datetime(data["fecha"].dt.strftime('%d-%m-%Y'))

# Calculamos los datos diarios como la diferencia de los totales
data['casos_24h']=data["casos_tot"].diff()
data['fallecidos_24h']=data["fallecidos_tot"].diff()

# Ponemos la fecha como indice, añadimos los días que faltan y volvemos a quitar la fecha como indice
data=data.set_index("fecha")
data=data.resample("D").asfreq()
data=data.reset_index()

# data.head(10)

# print(data.dtypes)


# In[3]:


# Calculamos la indicencia a 14 dias

IA_14d=[None]*13

for i in data.index[13:]:
    if (not np.isnan(data["casos_24h"].iloc[i])):
        IA_14d.append("{:.2f}".format(data["casos_24h"].iloc[i+1-14:i+1].sum()*1e5/47351567))
    else:
        IA_14d.append(None)

IA_14d=np.array(IA_14d,dtype=float)

data["IA_14d"]=IA_14d

# data.tail(5)


# In[4]:


# Calculamos la indicencia a 7 dias

IA_7d=[None]*6

for i in data.index[6:]:
    if (not np.isnan(data["casos_24h"].iloc[i])):
        IA_7d.append("{:.2f}".format(data["casos_24h"].iloc[i+1-7:i+1].sum()*1e5/47351567))
    else:
        IA_7d.append(None)

IA_7d=np.array(IA_7d,dtype=float)

data["IA_7d"]=IA_7d

# data=data.set_index("fecha")

# data.tail(5)


# In[5]:


# Ponemos la fecha como indice
data=data.set_index("fecha")


# In[6]:


# Sumamos los datos semanalmente
data_sem=data.resample('W').sum()
data_sem.drop("casos_tot",axis=1,inplace=True)
data_sem.drop("fallecidos_tot",axis=1,inplace=True)
data_sem.drop("IA_14d",axis=1,inplace=True)
data_sem.drop("IA_7d",axis=1,inplace=True)
# data_sem


# In[7]:


# Guardamos las tablas en un fichero .csv
data_temp2=data[["casos_24h","fallecidos_24h","IA_14d","IA_7d"]].copy()
data_temp2=data_temp2.dropna()
data_temp2.to_csv(path_or_buf="data_ESP_alltime.csv")

data_temp=data[["UCI","hospitalizados"]].copy()
data_temp=data_temp.dropna()
data_temp.to_csv(path_or_buf="data_ESP_hospUCI.csv")


data.to_csv(path_or_buf="data_ESP_noNULL.csv")

data_sem[["casos_24h","fallecidos_24h"]].to_csv(path_or_buf="data_ESP_sem.csv")

print("------ Finish datos Ministerio ESP!!!! --------")


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

# Consulta tabla con datos introduccidos manualmente de la Generalitat. Datos diarios separados por rango de edad y sezo.
con=sqlite3.connect('bases_datos/COVID_CV_GVA.db')

#----------------------------------------------------------------------------
# Datos agrupados para rango de edad y sexo
#----------------------------------------------------------------------------

data=pd.read_sql_query("""
                        SELECT fecha,SUM(acumulados_caso) AS casos_tot,SUM(acumulado_fallecidos) AS fallecidos_tot
                        FROM COVID_CV_GVA
                        GROUP BY fecha
                        """,con)


# Pasamos la fecha como indice y lo pasamos a formato fecha
data=data.set_index("fecha")
data.index = pd.to_datetime(data.index)

# Calculamos casos y fallecidos cada 24h
data['casos_24h']=data["casos_tot"].diff()
data['fallecidos_24h']=data["fallecidos_tot"].diff()

# Copiamos la tabla antes de rellenar los huecos para usarla posteriormente.
temp=data.copy()

# Rellenamos las fechas que faltan y volvemos a poner la fecha como columna en vez de indice.
data=data.resample("D").asfreq()

# Redistribuimos los datos entre los valores NULL en las columnas de casos_24h y fallecidos_24h
cols_red = ['casos_24h','fallecidos_24h']

data_temp=data.copy()
csum, fsum = data_temp[cols_red].sum()

print ("** REDISTRIBUTE MISSING VALUES CASOS/FALLECIDOS AGUPADOS**")
data_red = redistribute_nan (data_temp,columns=cols_red)
csum_red, fsum_red = data_red[cols_red].sum()

print ("** TOTAL SUM **")
print("before", int(csum), int(fsum))
print("after", int(csum_red), int(fsum_red), '\n')


# Calculamos la indicencia a 14 dias
data_red=data_red.reset_index()
IA_14d=[None]*13

for i in data_red.index[13:]:
    if (not np.isnan(data_red["casos_24h"].iloc[i])):
        IA_14d.append("{:.2f}".format(data_red["casos_24h"].iloc[i+1-14:i+1].sum()*1e5/4.975e6))
    else:
        IA_14d.append(None)

IA_14d=np.array(IA_14d,dtype=float)

data_red["IA_14d"]=IA_14d

# Calculamos la indicencia a 7 días
IA_7d=[None]*6

for i in data_red.index[6:]:
    if (not np.isnan(data_red["casos_24h"].iloc[i])):
        IA_7d.append("{:.2f}".format(data_red["casos_24h"].iloc[i+1-7:i+1].sum()*1e5/4.975e6))
    else:
        IA_7d.append(None)

IA_7d=np.array(IA_7d,dtype=float)

data_red["IA_7d"]=IA_7d


# Volvemos a poner la columna de fecha como indice
data_red=data_red.set_index("fecha")

# Sumamos los datos semanalmente
data_sem=data_red.resample('W').sum()
data_sem.drop("casos_tot",axis=1,inplace=True)
data_sem.drop("fallecidos_tot",axis=1,inplace=True)
data_sem.drop("IA_14d",axis=1,inplace=True)
data_sem.drop("IA_7d",axis=1,inplace=True)

# guardamos el resultado de haber agrupado por edades y sexo, haber tratado los datos y las inicidencias en una tabla csv
data_red.to_csv(path_or_buf="tablas_temp/datos_CV.csv")

# Guardamos en otra tabla csv los datos semanales
data_sem.to_csv(path_or_buf="tablas_temp/datos_CV_sem.csv")

#--------------------------------------------------------------------------------
# Datos agrupados de rango de edad para mujeres
#--------------------------------------------------------------------------------
data_mujer=pd.read_sql_query("""
                        SELECT fecha,sexo,SUM(acumulados_caso) AS casos_tot,SUM(acumulado_fallecidos) AS fallecidos_tot
                        FROM COVID_CV_GVA
                        WHERE sexo="Mujer"
                        GROUP BY fecha
                        """,con)


# Combertimos la fecha en indice y la pasamos a formato fecha
data_mujer=data_mujer.set_index("fecha")
data_mujer.index = pd.to_datetime(data_mujer.index)

# Calculamos los casos y los fallecidos en 24h
data_mujer['casos_24h']=data_mujer["casos_tot"].diff()
data_mujer['fallecidos_24h']=data_mujer["fallecidos_tot"].diff()

# Rellenamos las fechas que faltan
data_mujer=data_mujer.resample("D").asfreq()

# Eliminamos la columna donde indica el sexo
data_mujer.drop("sexo",axis=1,inplace=True)

# Redistribuimos los datos entre los valores NULL en las columnas de casos_24h y fallecidos_24h
cols_red = ['casos_24h','fallecidos_24h']

data_temp_mujer=data_mujer.copy()
csum, fsum = data_temp_mujer[cols_red].sum()

print ("** REDISTRIBUTE MISSING VALUES CASOS/FALLECIDOS MUJERES **")
data_red_mujer = redistribute_nan (data_temp_mujer,columns=cols_red)
csum_red, fsum_red = data_red_mujer[cols_red].sum()

print ("** TOTAL SUM **")
print("before", int(csum), int(fsum))
print("after", int(csum_red), int(fsum_red), '\n')


#--------------------------------------------------------------------------------
# Datos agrupados de rango de edad para hombres 
#--------------------------------------------------------------------------------

data_hombre=pd.read_sql_query("""
                        SELECT fecha,sexo,SUM(acumulados_caso) AS casos_tot,SUM(acumulado_fallecidos) AS fallecidos_tot
                        FROM COVID_CV_GVA
                        WHERE sexo="Hombre"
                        GROUP BY fecha
                        """,con)


# Combertimos la fecha en indice y la pasamos a formato fecha
data_hombre=data_hombre.set_index("fecha")
data_hombre.index = pd.to_datetime(data_hombre.index)

# Calculamos los casos y los fallecidos en 24h
data_hombre['casos_24h']=data_hombre["casos_tot"].diff()
data_hombre['fallecidos_24h']=data_hombre["fallecidos_tot"].diff()

# Rellenamos las fechas que faltan
data_hombre=data_hombre.resample("D").asfreq()

# Eliminamos la columna donde indica el sexo
data_hombre.drop("sexo",axis=1,inplace=True)

# Redistribuimos los datos entre los valores NULL en las columnas de casos_24h y fallecidos_24h
cols_red = ['casos_24h','fallecidos_24h']

data_temp_hombre=data_hombre.copy()
csum, fsum = data_temp_hombre[cols_red].sum()

print ("** REDISTRIBUTE MISSING VALUES CASOS/FALLECIDOS HOMBRES **")
data_red_hombre = redistribute_nan (data_temp_hombre,columns=cols_red)
csum_red, fsum_red = data_red_hombre[cols_red].sum()

print ("** TOTAL SUM **")
print("before", int(csum), int(fsum))
print("after", int(csum_red), int(fsum_red), '\n')


# Creamos una tabla con los datos de casos y fallecidos en 24h para hombres y mujeres separados en columnas

# Copio la tabla de datos de la mujer a la que eliminamos la columna de sexo 
data_sexo=data_red_mujer.copy()

# Cambio el nombre de las columnas
data_sexo.rename(columns={"casos_24h": "casos_24h_mujer", "fallecidos_24h": "fallecidos_24h_mujer",
                         "casos_tot": "casos_tot_mujer","fallecidos_tot": "fallecidos_tot_mujer"},inplace=True)

# Añadimos a la tabla los datos del hombre
data_sexo["casos_tot_hombre"]=data_red_hombre["casos_tot"]
data_sexo["fallecidos_tot_hombre"]=data_red_hombre["fallecidos_tot"]
data_sexo["casos_24h_hombre"]=data_red_hombre["casos_24h"]
data_sexo["fallecidos_24h_hombre"]=data_red_hombre["fallecidos_24h"]

# Guardamos la tabla en un csv
data_sexo[["casos_24h_mujer","fallecidos_24h_mujer","casos_24h_hombre","fallecidos_24h_hombre"]].to_csv(path_or_buf="tablas_temp/datos_CV_hombre_mujer.csv")

# -----------------------------------------------------------------------------------------
# IA 14d por sexo
#---------------------------------------------------------------------------------------

poblacion_sexo=[2566744,2491394]
d=["fallecidos_24h_mujer","fallecidos_24h_hombre","casos_24h_mujer","casos_24h_hombre","casos_tot_hombre","fallecidos_tot_hombre","casos_tot_mujer","fallecidos_tot_mujer"]
a=["casos_24h_mujer","casos_24h_hombre"]
b=["IA_14d_mujer","IA_14d_hombre"]

# Eliminamos el indice de las fechas para poder operar con la tabla
data_sexo=data_sexo.reset_index()

# Creamos un DataFrame solo con fechas donde guardaremos la IA 14d por rango de edad
IA_14d_sexo=data_sexo.copy()
for j in list(range(len(d))):
    IA_14d_sexo.drop(d[j],axis=1,inplace=True) 
    
# Calculo de la IA 14d por rango de edad
for j in list(range(len(a))):
    IA_temp_sexo=[None]*13
    
    for i in data_sexo[a[j]].index[13:]:
        if (not np.isnan(data_sexo[a[j]].iloc[i])):
            IA_temp_sexo.append("{:.2f}".format(data_sexo[a[j]].iloc[i+1-14:i+1].sum()*1e5/poblacion_sexo[j]))
        else:
            IA_temp_sexo.append(None)
        
    IA_temp_sexo=np.array(IA_temp_sexo,dtype=float)
    IA_14d_sexo[b[j]]=IA_temp_sexo


# Volvemos a poner el indice de las fechas
data_sexo=data_sexo.set_index("fecha")
IA_14d_sexo=IA_14d_sexo.set_index("fecha")


# Guardamos la tabla en un csv
IA_14d_sexo.to_csv(path_or_buf="tablas_temp/datos_CV_IA_14d_sexo.csv")


#--------------------------------------------------------------------------------
# Datos agregados de sexo para cada rango de edad
#--------------------------------------------------------------------------------

data_edad=pd.read_sql_query("""
                        SELECT fecha,edad,SUM(acumulados_caso) AS casos_tot,SUM(acumulado_fallecidos) AS fallecidos_tot
                        FROM COVID_CV_GVA
                        GROUP BY fecha,edad
                        """,con)

# Calculamos los casos acumulados cada 24h
cs_24h_edad=[None]*len(data_edad.index)
for i in data_edad.index[10:]:
    cs_24h_edad[i]=data_edad["casos_tot"].iloc[i]-data_edad["casos_tot"].iloc[i-10]
    data_edad["casos_24h"]=cs_24h_edad
    
# Calculamos los fallecidos cada 24h
f_24h_edad=[None]*len(data_edad.index)
for i in data_edad.index[10:]:
    f_24h_edad[i]=data_edad["fallecidos_tot"].iloc[i]-data_edad["fallecidos_tot"].iloc[i-10]
    data_edad["fallecidos_24h"]=f_24h_edad


# Creamos una tabla nueva solo con los casos cada 24h donde cada columna es una franja de edad

# Hacemos una copia de la tabla de la consulta de las edades para trabajar sobre ella. Si en vez de usar .copy()
# usamos = se crea un enlace y cuando modifiquemos una también se modificará la otra.
casos_24h_edad=data_edad.copy()

# Eliminamos de las columnas que no nos interesan
casos_24h_edad.drop("fallecidos_tot",axis=1,inplace=True)
casos_24h_edad.drop("casos_tot",axis=1,inplace=True)
casos_24h_edad.drop("fallecidos_24h",axis=1,inplace=True)

# Pasamos cada fila de edad a una columna
casos_24h_edad=casos_24h_edad.pivot(index='fecha', columns='edad', values='casos_24h')

# Convertimos el indice en formato fecha y rellenamos los días que faltan 
casos_24h_edad.index= pd.to_datetime(casos_24h_edad.index)
casos_24h_edad=casos_24h_edad.resample("D").asfreq()

# Redistribuimos los datos entre los valores NULL en las columnas de casos_24h y fallecidos_24h
cols_red = ["0-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80-89","90+"]

data_temp_casos_edad=casos_24h_edad.copy()

print ("** REDISTRIBUTE MISSING VALUES CASOS EDAD**")
data_red_casos_edad = redistribute_nan (data_temp_casos_edad,columns=cols_red)

# Guardamos la tabla en un csv
data_red_casos_edad.to_csv(path_or_buf="tablas_temp/datos_CV_casos_edad.csv")


# Creamos una tabla nueva solo con los fallecidos cada 24h donde cada columna es una franja de edad

# Hacemos una copia de la tabla por edades para no modificar la original
fallecidos_24h_edad=data_edad.copy()

# Eliminamos los datos que no vamos a usar
fallecidos_24h_edad.drop("fallecidos_tot",axis=1,inplace=True)
fallecidos_24h_edad.drop("casos_tot",axis=1,inplace=True)
fallecidos_24h_edad.drop("casos_24h",axis=1,inplace=True)

# Pasamos cada fila de edad a una columna
fallecidos_24h_edad=fallecidos_24h_edad.pivot(index='fecha', columns='edad', values='fallecidos_24h')

# Convertimos la fecha a formato datos y rellenamos los datos que no hay
fallecidos_24h_edad.index= pd.to_datetime(fallecidos_24h_edad.index)
fallecidos_24h_edad=fallecidos_24h_edad.resample("D").asfreq()

# Redistribuimos los datos entre los valores NULL en las columnas de casos_24h y fallecidos_24h
cols_red = ["0-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80-89","90+"]

data_temp_fallecidos_edad=fallecidos_24h_edad.copy()

print ("** REDISTRIBUTE MISSING VALUES FALLECIDOS EDAD**")
data_red_fallecidos_edad = redistribute_nan (data_temp_fallecidos_edad,columns=cols_red)


# Guardamos la tabla en un csv
data_red_fallecidos_edad.to_csv(path_or_buf="tablas_temp/datos_CV_fallecidos_edad.csv")



# -----------------------------------------------------------------------------------------
# IA 14d por rango de edad
#---------------------------------------------------------------------------------------

poblacion_edad=[441303,540113,516278,627111,849342,763828,597320,435684,235556,51603]
a=["0-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80-89","90+"]

# Eliminamos el indice de las fechas para poder operar con la tabla
data_red_casos_edad=data_red_casos_edad.reset_index()

# Creamos un DataFrame solo con fechas donde guardaremos la IA 14d por rango de edad
IA_14d_edad=data_red_casos_edad.copy()
for j in list(range(len(a))):
    IA_14d_edad.drop(a[j],axis=1,inplace=True)  
    
# Calculo de la IA 14d por rango de edad
for j in list(range(len(a))):
    IA_temp_edad=[None]*13
    
    for i in data_red_casos_edad[a[j]].index[13:]:
        if (not np.isnan(data_red_casos_edad[a[j]].iloc[i])):
            IA_temp_edad.append("{:.2f}".format(data_red_casos_edad[a[j]].iloc[i+1-14:i+1].sum()*1e5/poblacion_edad[j]))
        else:
            IA_temp_edad.append(None)
        
    IA_temp_edad=np.array(IA_temp_edad,dtype=float)
    IA_14d_edad[a[j]]=IA_temp_edad


# Volvemos a poner el indice de las fechas
data_red_casos_edad=data_red_casos_edad.set_index("fecha")



IA_14d_edad=IA_14d_edad.set_index("fecha")
#IA_14d_edad.tail(10)

# Guardamos la tabla en un csv
IA_14d_edad.to_csv(path_or_buf="tablas_temp/datos_CV_IA_14d_edad.csv")



#-------------------------------------------------------------
# % de casos por rango de edad
#-------------------------------------------------------------

# Creamos una nueva tabla donde vamos a calcular el porcentaje respecto a los casos totales de ese día de los casos
# de cada rango de edad. Para ello usamos dos tablas:

# data_edad: Tabla con datos separados por edades
# temp: Tabla con datos en la que se ha sumado los datos de edad y sexo

por_casos_24h=[None]*len(data_edad.index)

for i in data_edad.index[10:]:
    por_casos_24h[i]=(data_edad["casos_24h"].iloc[i]/temp['casos_24h'].iloc[int(i/10)])*100

data_edad["por_casos_24h"]=por_casos_24h


# Creamos una nueva tabla donde vamos a calcular el porcentaje respecto a los fallecidos totales de ese día de 
# los casos de cada rango de edad. Para ello usamos dos tablas:

# data_edad: Tabla con datos separados por edades
# temp: Tabla con datos en la que se ha sumado los datos de edad y sexo

por_fallecidos_24h=[None]*len(data_edad.index)

for i in data_edad.index[10:]:
    por_fallecidos_24h[i]=(data_edad["fallecidos_24h"].iloc[i]/temp['fallecidos_24h'].iloc[int(i/10)])*100

data_edad["por_fallecidos_24h"]=por_fallecidos_24h


# Creamos una tabla nueva solo con el porcentaje de los casos cada 24h donde cada columna es una franja de edad

# Hacemos una copia de la tabla de la consulta de las edades para trabajar sobre ella.
por_casos_24h_edad=data_edad.copy()

# Eliminamos los datos que no vamos a usar
por_casos_24h_edad.drop("fallecidos_tot",axis=1,inplace=True)
por_casos_24h_edad.drop("fallecidos_24h",axis=1,inplace=True)
por_casos_24h_edad.drop("por_fallecidos_24h",axis=1,inplace=True)
por_casos_24h_edad.drop("casos_tot",axis=1,inplace=True)
por_casos_24h_edad.drop("casos_24h",axis=1,inplace=True)

# Pasamos cada fila de edad a una columna
por_casos_24h_edad=por_casos_24h_edad.pivot(index='fecha', columns='edad', values='por_casos_24h')
por_casos_24h_edad.head(20)

# Convertimos la fecha a formato datos y rellenamos los datos que no hay
por_casos_24h_edad.index= pd.to_datetime(por_casos_24h_edad.index)
por_casos_24h_edad=por_casos_24h_edad.resample("D").asfreq()

# Guardamos la tabla en un csv
por_casos_24h_edad.to_csv(path_or_buf="tablas_temp/datos_CV_por_casos_edad.csv")


#-------------------------------------------------------------
# % de fallecidos por rango de edad
#-------------------------------------------------------------

# Creamos una tabla nueva solo con el porcentaje de los fallecidos cada 24h donde cada columna es una franja de edad

# Hacemos una copia de la tabla de la consulta de las edades para trabajar sobre ella.
por_fallecidos_24h_edad=data_edad.copy()

# Eliminamos los datos que no vamos a usar
por_fallecidos_24h_edad.drop("fallecidos_tot",axis=1,inplace=True)
por_fallecidos_24h_edad.drop("fallecidos_24h",axis=1,inplace=True)
por_fallecidos_24h_edad.drop("casos_tot",axis=1,inplace=True)
por_fallecidos_24h_edad.drop("casos_24h",axis=1,inplace=True)
por_fallecidos_24h_edad.drop("por_casos_24h",axis=1,inplace=True)

# Pasamos cada fila de edad a una columna
por_fallecidos_24h_edad=por_fallecidos_24h_edad.pivot(index='fecha', columns='edad', values='por_fallecidos_24h')

# Convertimos la fecha a formato datos y rellenamos los datos que no hay
por_fallecidos_24h_edad.index= pd.to_datetime(por_fallecidos_24h_edad.index)
por_fallecidos_24h_edad=por_fallecidos_24h_edad.resample("D").asfreq()

# Guardamos la tabla en un csv
por_fallecidos_24h_edad.to_csv(path_or_buf="tablas_temp/datos_CV_por_fallecidos_edad.csv")


print(" ----- Datos de la C. Valenciana del GVA terminado----------")

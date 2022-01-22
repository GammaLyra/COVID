import pandas as pd
import numpy as np
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import matplotlib.dates as mdates
from statsmodels.tsa.seasonal import seasonal_decompose


# Leemos los datos del fichero csv
file1_path="tablas_ini/vacunados_1dosis_210621.csv"
vac_1dosis_ESP=pd.read_csv(file1_path,converters={"fecha":pd.to_datetime})

file2_path="tablas_ini/vacunados_2dosis_210621.csv"
vac_2dosis_ESP=pd.read_csv(file2_path,converters={"fecha":pd.to_datetime})



# Ponemos la comunidad como indice
vac_1dosis_ESP=vac_1dosis_ESP.set_index("Comunidad")
vac_2dosis_ESP=vac_2dosis_ESP.set_index("Comunidad")

# Calculamos el porcentaje total de la población Española y de la C. Valenciana que está vacunada
vac_1dosis_ESP["tot_vac"].loc["España"]=(vac_1dosis_ESP["tot_vac"].loc["España"]/47450795)*100
vac_2dosis_ESP["tot_vac"].loc["España"]=(vac_2dosis_ESP["tot_vac"].loc["España"]/47450795)*100


vac_1dosis_ESP["tot_vac"].loc["C. Valenciana"]=(vac_1dosis_ESP["tot_vac"].loc["C. Valenciana"]/5057353)*100
vac_2dosis_ESP["tot_vac"].loc["C. Valenciana"]=(vac_2dosis_ESP["tot_vac"].loc["C. Valenciana"]/5057353)*100


#------------------------------------------------------------------------------------------------------
# Creamos una tabla con los datos de la C. Valenciana y España del último día para 1 dosis
#------------------------------------------------------------------------------------------------------


# Primero trabajamos con la tabla de 1 dosis
df1=vac_1dosis_ESP.copy()

# Quitamos la columna de la comunidad como indice
df1=df1.reset_index()

# Selecionamos los datos de la C. Valenciana y España 
df1=df1.loc[((df1['Comunidad'] == "C. Valenciana") | (df1['Comunidad'] == "España"))]

# Nos quedamos solo con los datos del último día
df1=df1.iloc[-2:]

# Eliminamos los datos que no vamos a usar
df1.drop("fecha",axis=1,inplace=True)
df1.drop("vac_80+",axis=1,inplace=True)
df1.drop("vac_70-79",axis=1,inplace=True)
df1.drop("vac_60-69",axis=1,inplace=True)
df1.drop("vac_50-59",axis=1,inplace=True)
df1.drop("vac_40-49",axis=1,inplace=True)
df1.drop("vac_30-39",axis=1,inplace=True)
df1.drop("vac_20-29",axis=1,inplace=True)
df1.drop("vac_12-19",axis=1,inplace=True)
df1.drop("vac_5-11",axis=1,inplace=True)
df1.drop("pobl_tot",axis=1,inplace=True)


# Trasponemos la tabla y cambiamos el nombre de las filas y las columnas. El nuevo indice serán los rangos de edad
df1=df1.set_index("Comunidad")
df1=df1.transpose()
df1=df1.reset_index()

df1 = df1.rename(columns={'index': 'edad'})
df1 = df1.rename(columns={'C. Valenciana': 'C. Valenciana - 1 dosis'})
df1 = df1.rename(columns={'España': 'España - 1 dosis'})
df1=df1.set_index("edad")
df1 = df1.rename({"por_80+":"80+", "por_70-79":"70-79", "por_60-69":"60-69",
                 "por_50-59":"50-59", "por_40-49":"40-49", "por_30-39":"30-39",
                 "por_20-29":"20-29", "por_12-19":"12-19", "por_5-11":"5-11", "por_tot":"pobl. vac.","tot_vac":"poblacion total"}, axis='index')



# Hacemos lo mismo pero para las dos dosis
df2=vac_2dosis_ESP.copy()
df2=df2.reset_index()

df2=df2.loc[((df2['Comunidad'] == "C. Valenciana") | (df2['Comunidad'] == "España"))]

df2=df2.iloc[-2:]

df2.drop("fecha",axis=1,inplace=True)
df2.drop("vac_80+",axis=1,inplace=True)
df2.drop("vac_70-79",axis=1,inplace=True)
df2.drop("vac_60-69",axis=1,inplace=True)
df2.drop("vac_50-59",axis=1,inplace=True)
df2.drop("vac_40-49",axis=1,inplace=True)
df2.drop("vac_30-39",axis=1,inplace=True)
df2.drop("vac_20-29",axis=1,inplace=True)
df2.drop("vac_12-19",axis=1,inplace=True)
df2.drop("vac_5-11",axis=1,inplace=True)
df2.drop("pobl_tot",axis=1,inplace=True)


df2=df2.set_index("Comunidad")
df2=df2.transpose()
df2=df2.reset_index()

df2 = df2.rename(columns={'index': 'edad'})
df2 = df2.rename(columns={'C. Valenciana': 'C. Valenciana - 2 dosis'})
df2 = df2.rename(columns={'España': 'España - 2 dosis'})
df2 = df2.set_index("edad")
df2 = df2.rename({"por_80+":"80+", "por_70-79":"70-79", "por_60-69":"60-69",
                 "por_50-59":"50-59", "por_40-49":"40-49", "por_30-39":"30-39",
                 "por_20-29":"20-29", "por_12-19":"12-19", "por_5-11":"5-11", "por_tot":"pobl. vac.","tot_vac":"poblacion total"}, axis='index')




# Unimos las dos tablas que acabamos de crear y las guardamos en una tabla csv
df_new=pd.concat([df1,df2],axis=1)
df_new.to_csv(path_or_buf="tablas_temp/vac_ESP_VAL_lastday.csv")


#------------------------------------------------------------------------------------------------------
# Creamos una tabla que contenga los datos de la C. Valenciana para todos los días
#------------------------------------------------------------------------------------------------------

# Primero trabajamos con la tabla de 1 dosis
vac_VAL_1dosis=vac_1dosis_ESP.copy()
vac_VAL_1dosis=vac_VAL_1dosis.reset_index()
vac_VAL_1dosis=vac_VAL_1dosis.set_index("fecha")

# Selecionamos solo los datos de la comunidad de Valencia
vac_VAL_1dosis=vac_VAL_1dosis.loc[(vac_VAL_1dosis['Comunidad'] == "C. Valenciana")]

# Eliminamos los datos que no vamos a usar
vac_VAL_1dosis.drop("Comunidad",axis=1,inplace=True)
vac_VAL_1dosis.drop("vac_80+",axis=1,inplace=True)
vac_VAL_1dosis.drop("vac_70-79",axis=1,inplace=True)
vac_VAL_1dosis.drop("vac_60-69",axis=1,inplace=True)
vac_VAL_1dosis.drop("vac_50-59",axis=1,inplace=True)
vac_VAL_1dosis.drop("vac_40-49",axis=1,inplace=True)
vac_VAL_1dosis.drop("vac_30-39",axis=1,inplace=True)
vac_VAL_1dosis.drop("vac_20-29",axis=1,inplace=True)
vac_VAL_1dosis.drop("vac_12-19",axis=1,inplace=True)
vac_VAL_1dosis.drop("vac_5-11",axis=1,inplace=True)
vac_VAL_1dosis.drop("por_tot",axis=1,inplace=True)

#vac_VAL_1dosis.drop("tot_vac",axis=1,inplace=True)
vac_VAL_1dosis.drop("pobl_tot",axis=1,inplace=True)

# Renombramos las columnas
vac_VAL_1dosis = vac_VAL_1dosis.rename(columns={"por_80+":"80+ 1dosis", "por_70-79":"70-79 1dosis", "por_60-69":"60-69 1dosis",
                 "por_50-59":"50-59 1dosis", "por_40-49":"40-49 1dosis", "por_30-39":"30-39 1dosis",
                 "por_20-29":"20-29 1dosis", "por_12-19":"12-19 1dosis", "por_5-11":"5-11 1dosis","tot_vac":"total 1 dosis"})


# Hacemos lo mismo que acabamos de hacer pero para la 2 dosis
vac_VAL_2dosis=vac_2dosis_ESP.copy()
vac_VAL_2dosis=vac_VAL_2dosis.reset_index()
vac_VAL_2dosis=vac_VAL_2dosis.set_index("fecha")


vac_VAL_2dosis=vac_VAL_2dosis.loc[(vac_VAL_2dosis['Comunidad'] == "C. Valenciana")]


vac_VAL_2dosis.drop("Comunidad",axis=1,inplace=True)
vac_VAL_2dosis.drop("vac_80+",axis=1,inplace=True)
vac_VAL_2dosis.drop("vac_70-79",axis=1,inplace=True)
vac_VAL_2dosis.drop("vac_60-69",axis=1,inplace=True)
vac_VAL_2dosis.drop("vac_50-59",axis=1,inplace=True)
vac_VAL_2dosis.drop("vac_40-49",axis=1,inplace=True)
vac_VAL_2dosis.drop("vac_30-39",axis=1,inplace=True)
vac_VAL_2dosis.drop("vac_20-29",axis=1,inplace=True)
vac_VAL_2dosis.drop("vac_12-19",axis=1,inplace=True)
vac_VAL_2dosis.drop("vac_5-11",axis=1,inplace=True)
vac_VAL_2dosis.drop("por_tot",axis=1,inplace=True)

#vac_VAL_2dosis.drop("tot_vac",axis=1,inplace=True)
vac_VAL_2dosis.drop("pobl_tot",axis=1,inplace=True)

vac_VAL_2dosis = vac_VAL_2dosis.rename(columns={"por_80+":"80+ 2dosis", "por_70-79":"70-79 2dosis", "por_60-69":"60-69 2dosis",
                 "por_50-59":"50-59 2dosis", "por_40-49":"40-49 2dosis", "por_30-39":"30-39 2dosis",
                 "por_20-29":"20-29 2dosis", "por_12-19":"12-19 2dosis", "por_5-11":"5-11 2dosis","tot_vac":"total 2 dosis"})

# Guardamos los resultados en una tabla csv
vac_VAL=pd.concat([vac_VAL_1dosis,vac_VAL_2dosis],axis=1)
vac_VAL.to_csv(path_or_buf="tablas_temp/vac_VAL_all_days.csv")


#------------------------------------------------------------------------------------------------------
# Creamos una tabla que contenga los datos de España para todos los días
#------------------------------------------------------------------------------------------------------

# Primero trabajamos con la tabla de 1 dosis
vac_ESP_1dosis=vac_1dosis_ESP.copy()
vac_ESP_1dosis=vac_ESP_1dosis.reset_index()
vac_ESP_1dosis=vac_ESP_1dosis.set_index("fecha")

# Selecionamos solo los datos de la comunidad de Valencia
vac_ESP_1dosis=vac_ESP_1dosis.loc[(vac_ESP_1dosis['Comunidad'] == "España")]

# Eliminamos los datos que no vamos a usar
vac_ESP_1dosis.drop("Comunidad",axis=1,inplace=True)
vac_ESP_1dosis.drop("vac_80+",axis=1,inplace=True)
vac_ESP_1dosis.drop("vac_70-79",axis=1,inplace=True)
vac_ESP_1dosis.drop("vac_60-69",axis=1,inplace=True)
vac_ESP_1dosis.drop("vac_50-59",axis=1,inplace=True)
vac_ESP_1dosis.drop("vac_40-49",axis=1,inplace=True)
vac_ESP_1dosis.drop("vac_30-39",axis=1,inplace=True)
vac_ESP_1dosis.drop("vac_20-29",axis=1,inplace=True)
vac_ESP_1dosis.drop("vac_12-19",axis=1,inplace=True)
vac_ESP_1dosis.drop("vac_5-11",axis=1,inplace=True)
vac_ESP_1dosis.drop("por_tot",axis=1,inplace=True)

#vac_ESP_1dosis.drop("tot_vac",axis=1,inplace=True)
vac_ESP_1dosis.drop("pobl_tot",axis=1,inplace=True)

# Renombramos las columnas
vac_ESP_1dosis = vac_ESP_1dosis.rename(columns={"por_80+":"80+ 1dosis", "por_70-79":"70-79 1dosis", "por_60-69":"60-69 1dosis",
                 "por_50-59":"50-59 1dosis", "por_40-49":"40-49 1dosis", "por_30-39":"30-39 1dosis",
                 "por_20-29":"20-29 1dosis", "por_12-19":"12-19 1dosis", "por_5-11":"5-11 1dosis","tot_vac":"total 1 dosis"})


# Hacemos lo mismo que acabamos de hacer pero para la 2 dosis
vac_ESP_2dosis=vac_2dosis_ESP.copy()
vac_ESP_2dosis=vac_ESP_2dosis.reset_index()
vac_ESP_2dosis=vac_ESP_2dosis.set_index("fecha")


vac_ESP_2dosis=vac_ESP_2dosis.loc[(vac_ESP_2dosis['Comunidad'] == "C. Valenciana")]


vac_ESP_2dosis.drop("Comunidad",axis=1,inplace=True)
vac_ESP_2dosis.drop("vac_80+",axis=1,inplace=True)
vac_ESP_2dosis.drop("vac_70-79",axis=1,inplace=True)
vac_ESP_2dosis.drop("vac_60-69",axis=1,inplace=True)
vac_ESP_2dosis.drop("vac_50-59",axis=1,inplace=True)
vac_ESP_2dosis.drop("vac_40-49",axis=1,inplace=True)
vac_ESP_2dosis.drop("vac_30-39",axis=1,inplace=True)
vac_ESP_2dosis.drop("vac_20-29",axis=1,inplace=True)
vac_ESP_2dosis.drop("vac_12-19",axis=1,inplace=True)
vac_ESP_2dosis.drop("vac_5-11",axis=1,inplace=True)
vac_ESP_2dosis.drop("por_tot",axis=1,inplace=True)

#vac_ESP_2dosis.drop("tot_vac",axis=1,inplace=True)
vac_ESP_2dosis.drop("pobl_tot",axis=1,inplace=True)

vac_ESP_2dosis = vac_ESP_2dosis.rename(columns={"por_80+":"80+ 2dosis", "por_70-79":"70-79 2dosis", "por_60-69":"60-69 2dosis",
                 "por_50-59":"50-59 2dosis", "por_40-49":"40-49 2dosis", "por_30-39":"30-39 2dosis",
                 "por_20-29":"20-29 2dosis", "por_12-19":"12-19 2dosis", "por_5-11":"5-11 2dosis","tot_vac":"total 2 dosis"})

# Guardamos los resultados en una tabla csv
vac_ESP=pd.concat([vac_ESP_1dosis,vac_ESP_2dosis],axis=1)
vac_ESP.to_csv(path_or_buf="tablas_temp/vac_ESP_all_days.csv")



print("------ Datos Vacunación terminado --------")


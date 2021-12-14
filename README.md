# COVID

1 - <b>Tablas iniciales</b>: Son las tablas (.csv) en las que manualmente subo los datos diarios que proporciona tanto la Generalitar como el Ministerio sobre los datos de COVID. 
  - <i>COVID_ESP_Ministerio.csv</i>: Datos diarios de España proporcionados por el Ministerio. Datos: Casos totales, Fallecidos totales, Ingresados totales en UCI, Hospitalizados totales
  - <i>COVID_CV_Ministerio.csv</i>: Datos diarios de la Comunidad de Valencia proporcionados por el Ministerio. Datos: IA 14d, IA7d, Casos totales, Fallecidos totales, % hospitalizaciones, % UCI, Ingresados totales en UCI, Hospitalizados totales. 
  - <i>COVID_CV_GVA.csv</i>: Datos diarios de la Comunidad de Valencia proporcionados por la Generalitat. Los datos están separados en rango de edad y sexo. Datos: Casos totales, Fallecidos totales, % casos totales, % fallecidos totales.
  - <i>vacunados_1dosis_210621.csv</i>: Datos diarios de España proporcionados por el Ministerio de personas vacunadas con la 1º dosis a partir del 21/06/2021. Datos separados por Comunidades y rango de edad. Datos: Población vacunada por rango de edad, % población vacunada por rango de edad, población total a vacunar, población total vacunada y % población total vacunada.  
  - <i>vacunados_2dosis_210621.csv</i>: Datos diarios de España proporcionados por el Ministerio de personas vacunadas con la 2º dosis a partir del 21/06/2021. Datos separados por Comunidades y rango de edad. Datos: Población vacunada por rango de edad, % población vacunada por rango de edad, población total a vacunar, población total vacunada y % población total vacunada.

2 -<b> Base de datos inicial</b>: Convertimos la tabla COVID_CV_GVA.csv en una base de datos .db usando sqlite para poder hacer consultas 


  
- <b> Scripts </b>:  
  - <i> Covid_CV_GVA_script.py</i>: 

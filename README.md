# COVID

<ol>
 <li> <b>Tablas iniciales</b>: Son las tablas (.csv) en las que manualmente subo los datos diarios que proporciona tanto la Generalitar como el Ministerio sobre los datos de COVID. </li>
    <ul>
      <li><i>COVID_ESP_Ministerio.csv</i>: Datos diarios de España proporcionados por el Ministerio. Datos: Casos acumulados, fallecidos acumulados, ingresados totales en UCI, hospitalizados totales</li> 
      <li><i>COVID_CV_Ministerio.csv</i>: Datos diarios de la Comunidad de Valencia proporcionados por el Ministerio. Datos: IA 14d, IA7d, casos acumulados, fallecidos acumulados, % hospitalizaciones, % UCI, ingresados totales en UCI, hospitalizados totales.</li>
      <li><i>COVID_CV_GVA.csv</i>: Datos diarios de la Comunidad de Valencia proporcionados por la Generalitat. Los datos están separados en rango de edad y sexo. Datos: Casos acumulados, fallecidos acumulados, % casos acumulados, % fallecidos acumulados.</li> 
      <li><i>vacunados_1dosis_210621.csv</i>: Datos diarios proporcionados por el Ministerio, personas vacunadas con la 1º dosis a partir del 21/06/2021. Datos separados por Comunidades y rango de edad. Datos: Población vacunada por rango de edad, % población vacunada por rango de edad, población total a vacunar, población total vacunada y % población total vacunada.</li> 
      <li><i>vacunados_2dosis_210621.csv</i>: Datos diarios de España proporcionados por el Ministerio de personas vacunadas con la 2º dosis a partir del 21/06/2021. Datos separados por Comunidades y rango de edad. Datos: Población vacunada por rango de edad, % población vacunada por rango de edad, población total a vacunar, población total vacunada y % población total vacunada.</li>
 </ul></li> 

 <li> <b> Base de datos parcial</b> (COVID_CV_GVA.db): La tabla inicial COVID_CV_GVA.csv se convierte en una base de datos (.db) para poder hacer consultas posteriores usando sqlite en Python. La conversión se hace usando un script de sqlite (creacion_BD_datos_GVA.sql)</li>

 <li><b> Scripts </b>:  
    <ul>
      <li><i> Covid_CV_GVA_script.py</i>: En este script se hacen diferentes consultas a la base de datos que acabamos de crear con los datos de la Generalitat para operar con los datos y se crean tablas con los datos de salida que nos interesan. Tablas de salida: 
      <ul>
        <li> datos_CV_GVA_agrupados.csv: Datos diarios sumando todos los rangos de edad y sexo. Se ha calculado la IA a 14d y a 7d, y los casos y fallecidos producidos ese día.</li>
        <li> datos_CV_GVA_agrupados_noNULL.csv: La misma tabla que la anterior pero se han eliminado las entradas que tienen NULLs. </li>
        <li> datos_semanales.csv: Casos y fallecidos acumulados durante 7 días. Datos calculados por nosotros.</li>
        <li> datos_hombre_mujer.csv: Casos y fallecidos diarios para mujeres y hombres por separado. </li>
        <li> casos_24h_edad.csv: Casos diarios para cada rango de edad</li>
        <li> fallecidos_24h_edad.csv Fallecidos diarios para cada rango de edad</li>
        <li> IA_14d_edad.csv: Incidencia acumulada a 14 días para cada rango de edad. Datos calculados por nosotros. </li>
        <li> por_casos_24h_edad.csv: Porcentaje de casos diarios para cada rango de edad respecto al total de casos diarios. Datos calculados por nosotros.</li>
        <li> por_fallecidos_24h_edad.csv: Porcentaje de fallecidos diarios para cada rango de edad respecto al total de fallecidos diarios. Datos calculados por nosotros. </li></ul></li>
      <li> <i>Covid_CV_Ministerio-script.py </i></li>
      <li> <i>Covid_ESP_Ministerio-script.py </i></li>
     <li> <i>Vacunacion_script.py <i></li></ul></li>
  <li> Creamos la base de datos completa </li>
</ol>

aaa

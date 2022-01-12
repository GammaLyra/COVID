# COVID en España y Comunidad Valenciana
###### Datos del Ministerior de Sanidad y la Generalitat de Valencìa
<hr>
<hr>

 <b><u>Tablas iniciales</u></b>: Son las tablas (.csv) en las que manualmente subimos los datos diarios que proporciona tanto la Generalitat como el Ministerio sobre los datos de COVID. </li>
    <ul>
      <li><i><b>COVID_ESP_Ministerio.csv</b></i>: Datos diarios de España proporcionados por el Ministerio. Datos: Casos acumulados, fallecidos acumulados, ingresados en UCI, hospitalizados.</li> 
      <li><i><b>COVID_CV_Ministerio.csv</b></i>: Datos diarios de la Comunidad de Valencia proporcionados por el Ministerio. Datos: IA 14d, IA7d, casos acumulados, fallecidos acumulados, % hospitalizaciones, % UCI, ingresados totales en UCI, hospitalizados totales.</li>
      <li><i><b>COVID_CV_GVA.csv</b></i>: Datos diarios de la Comunidad de Valencia proporcionados por la Generalitat. Los datos están separados en rango de edad y sexo. Datos: Casos acumulados, fallecidos acumulados, % casos acumulados, % fallecidos acumulados.</li> 
      <li><i><b>vacunados_1dosis_210621.csv:</b></i> [No actualizadas desde el 01/12/21 hasta el 11/01/22 - vacunación entre 5-12 años solo para C. Valenciana y España]´ Datos diarios proporcionados por el Ministerio, personas vacunadas con la 1º dosis a partir del 21/06/2021. Datos separados por Comunidades y rango de edad. Datos: Población vacunada por rango de edad, % población vacunada por rango de edad, población total a vacunar, población total vacunada y % población total vacunada.</li> 
      <li><i><b>vacunados_2dosis_210621.csv</b></i>: [No actualizadas desde el 01/12/21 hasta el 11/01/22 - vacunación entre 5-12 años solo para C. Valenciana y España] Datos diarios de España proporcionados por el Ministerio de personas vacunadas con la 2º dosis a partir del 21/06/2021. Datos separados por Comunidades y rango de edad. Datos: Población vacunada por rango de edad, % población vacunada por rango de edad, población total a vacunar, población total vacunada y % población total vacunada.</li>
 </ul>
 
 <hr>
 
 Antes de representar y analizar los datos creamos una base de datos que contendrá solo la información que nos interesa de las tablas anteriores y algunos datos extra que calculamos a partir de esos datos. Para ello haremos los siguientes pasos (el script <i>creacion_base_datos.txt</i> ejecuta todos estos pasos):

<ol>
 <li> <b> <u>Base de datos parcial</u> (COVID_CV_GVA.db)</b>: La tabla inicial <i>COVID_CV_GVA.csv<i> se convierte en una base de datos (.db) para poder hacer consultas. La conversión se hace usando un script de sqlite (<i>creacion_BD_datos_GVA.sql</i>)</li>

 <li><b> <u>Scripts Python</u> </b>:  
    <ul>
      <li><i> <b>Covid_CV_GVA_script.py</b></i>: En este script se hacen diferentes consultas usando sqlite a la base de datos que acabamos de crear (<i>COVID_CV_GVA.db</i>) con los datos de la Generalitat para operar con los datos y se crean tablas con los datos de salida que nos interesan. Tablas de salida: 
      <ul>
        <li> <i>datos_CV.csv</i>: Datos diarios sumando todos los rangos de edad y sexo. Se ha calculado la IA a 14d y a 7d, y los casos y fallecidos producidos ese día.</li>
        <li> <i>datos_CV_noNULL.csv</i>: La misma tabla que la anterior pero se han eliminado las entradas que tienen valores NULLs. </li>
        <li> <i>datos_CV_sem.csv</i>: Casos y fallecidos acumulados durante 7 días. Datos calculados por nosotros.</li>
        <li> <i>datos_CV_hombre_mujer.csv</i>: Casos y fallecidos diarios para mujeres y hombres por separado. </li>
        <li> <i>datos_CV_casos_edad.csv</i>: Casos diarios en cada rango de edad</li>
        <li> <i>datos_CV_fallecidos_edad.csv</i>: Fallecidos diarios en cada rango de edad</li>
        <li> <i>datos_CV_IA_14d_edad.csv</i>: Incidencia acumulada a 14 días en cada rango de edad. Datos calculados por nosotros. </li>
        <li> <i>datos_CV_por_casos_edad.csv</i>: Porcentaje de casos diarios en cada rango de edad respecto al total de casos diarios. Datos calculados por nosotros.</li>
        <li> <i>datos_CV_por_fallecidos_edad.csv</i>: Porcentaje de fallecidos diarios en cada rango de edad respecto al total de fallecidos diarios. Datos calculados por nosotros. </li></ul></li>
      <li> <i><b>Covid_CV_Ministerio-script.py</b>:</i> Lee la tabla inicial de los datos diarios del Ministerio para la comunidad de Valencia (<i>COVID_CV_Ministerio.csv</i>) y guardan en una tabla los datos de ingresados en UCI y hospitalizaciones. También se calcula los casos y fallecidos diarios, así como la IA a 14d y 7d, pero guardan puesto que no se utilizan. Para la Comunidad de Valencia se usan los datos proporcionados por la Generalitat (parecen más fiables), exceptuando hospitalizaciones y UCI que la GVA no los proporciona. Tabla de salida:
      <ul>
      	<li><i>datos_CV_hosp_UCI.csv</i>: Datos de hospitalizaciones y personas en UCI. Datos totales del día, no los que han ingresado nuevos ese día. </li>
        </ul></li>   
      <li> <b><i>Covid_ESP_Ministerio-script.py</i></b>: Lee la tabla inicial de los datos para España del Ministerio (<i>COVID_CV_Ministerio.csv</i>), se calcula los casos y fallecidos diarios a partir de los acumulados, la IA a 14d y 7d, y por último se calcula los casos y fallecidos semanalmente. Todo ello se guarda en diferentes tablas. Tablas de salida: 
      <ul>
      <li><i>datos_ESP.csv: Datos diarios de casos y fallecidos durante ese día e incidencia acumulada a 14 días y 7 días. Datos calculados por nosotros.</i></li>
      <li><i>datos_ESP_noNULL.csv:</i> Lo mismo que la tabla anterior pero se han eliminado las entradas que contienen valores NULL.</li>
      <li><i>datos_ESP_hosp_UCI.csv:</i> Datos diarios de hospitalizaciones y hospitalizaciones en UCI. Datos totales del día, no los que han ingresado nuevos ese día. </li>
      <li><i>datos_ESP_sem.csv:</i> Casos y fallecidos acumulados durante 7 días. Datos calculados por nosotros.</li>
      </ul></li>      
     <li> <b><i>Vacunacion_script.py<i></b>: Lee las tablas iniciales de vacunación en España (<i>vacunados_1dosis_210621.csv</i> y <i>vacunados_2dosis_210621.csv</i>) y guarda en dos tablas los datos que nos interesan sobre la vacunación. Tablas de salida:
     <ul>
     <li><i>vac_ESP_VAL_lastday.csv</i>: Contiene los datos sobre el porcentaje de población vacunada con 1 dosis y 2 dosis para España y la C. Valenciana en el último día.</li>
     <li><i>vac_VAL_all_days.csv</i>: Contiene los datos del porcentaje de población vacunada con 1 y 2 dosis en la C. Valenciana para todos los días desde el 21/06/2021.  </li
     </ul></li>
     </li></ul></ul>
     
  <li> Por último se usa un script de sqlite (<i>base_datos_completa.sql</i>) para crear la base de datos final con todas las tablas que acabamos de crear (<i><b>COVID.db</b></i>). Dentro de la base de datos las tablas tienen el mismo nombre que los .csv de los que provienen. </li>
</ol>

<hr>

Una vez que ya tenemos la base completa solo con los datos que nos interesa, lo siguiente que vamos a hacer es representar los datos y analizarlos. Para ello usamos notebooks de Jupyter en Python:

- <b>Representación de los datos</b>: El notebook es <i>representacion.ipynb</i>


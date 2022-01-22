# COVID en España y Comunidad Valenciana
###### Datos del Ministerior de Sanidad y la Generalitat de Valencìa
<hr>
<hr>

 <b><u>Tablas iniciales</u></b>: Son las tablas (.csv) en las que manualmente subimos los datos diarios que proporciona tanto la Generalitat como el Ministerio sobre los datos de COVID. </li>
    <ul>
      <li><i><b>COVID_ESP_Ministerio.csv</b></i>: Datos diarios de España proporcionados por el Ministerio. Datos: Casos acumulados, fallecidos acumulados, ingresados en UCI, hospitalizados.</li> 
      <li><i><b>COVID_CV_Ministerio.csv</b></i>: Datos diarios de la Comunidad de Valencia proporcionados por el Ministerio. Datos: IA 14d, IA7d, casos acumulados, fallecidos acumulados, % hospitalizaciones, % UCI, ingresados totales en UCI, hospitalizados totales.</li>
      <li><i><b>COVID_CV_GVA.csv</b></i>: Datos diarios de la Comunidad de Valencia proporcionados por la Generalitat. Los datos están separados en rango de edad y sexo. Datos: Casos acumulados, fallecidos acumulados, % casos acumulados, % fallecidos acumulados.</li> 
      <li><i><b>vacunados_1dosis_210621.csv:</b></i> [No datos desde el 01/12/21 hasta el 10/01/22. A partir del 11/01/22 solo actualizado para la C. Valenciana y España] Datos diarios proporcionados por el Ministerio, personas vacunadas con la 1º dosis a partir del 21/06/2021. Datos separados por Comunidades y rango de edad. Datos: Población vacunada por rango de edad, % población vacunada por rango de edad, población total a vacunar, población total vacunada y % población total vacunada.</li> 
      <li><i><b>vacunados_2dosis_210621.csv</b></i>: [No datos desde el 01/12/21 hasta el 10/01/22. A partir del 11/01/22 solo actualizado para la C. Valenciana y España] Datos diarios de España proporcionados por el Ministerio de personas vacunadas con la 2º dosis a partir del 21/06/2021. Datos separados por Comunidades y rango de edad. Datos: Población vacunada por rango de edad, % población vacunada por rango de edad, población total a vacunar, población total vacunada y % población total vacunada.</li>
 </ul>
 
 <hr>
 
 Antes de representar y analizar los datos creamos una base de datos que contendrá solo la información que nos interesa de las tablas anteriores y algunos datos extra que calculamos a partir de esos datos. Para ello haremos los siguientes pasos (el script <i>creacion_base_datos.txt</i> ejecuta todos estos pasos):

<ol>
 <li> <b> <u>Base de datos parcial</u> (COVID_CV_GVA.db)</b>: La tabla inicial <i>COVID_CV_GVA.csv<i> se convierte en una base de datos (.db) para poder hacer consultas. La conversión se hace usando un script de sqlite (<i>creacion_BD_datos_GVA.sql</i>)</li>

 <li><b> <u>Scripts Python</u> </b>:  
    <ul>
      <li><i> <b>Covid_CV_GVA_script.py</b></i>: Se hacen 3 consultas a la base de datos de la Generalitat (<i>COVID_CV_GVA.db</i>) usando sqlite: 1) Casos y fallecidos totales para todos los rangos de edad y sexo; 2) Casos y fallecidos totales para todos los rangos de edad separando entre hombres y mujeres; 3) Casos y fallecidos para todos los sexos, separando en rango de edad. En cada consulta se calcula los casos/fallecidos diarios y en algunos casos también se calcula los casos/fallecidos semanales y la incidencia a 14 días y 7 días. Los datos han sido tratados de tal forma que se han distribuido los casos/fallecidos diarios del día posterior a un fin de semana o festivo entre ese día y los días sin datos (la distribución se ha hecho de forma que el día con datos se queda el doble de casos/fallecidos que los días sin datos). Todos los datos se han guardado en diferentes tablas de salida. Tablas de salida: 
      <ul>
        <li> <i>datos_CV.csv</i>: Casos y fallecidos diarios, casos y fallecidos totales e incidencia acumulada a 14 días y 7 días.</li>
        <li> <i>datos_CV_sem.csv</i>: Casos y fallecidos acumulados durante 7 días. </li>
        <li> <i>datos_CV_hombre_mujer.csv</i>: Casos y fallecidos diarios para mujeres y hombres por separado. </li>
        <li> <i>datos_CV_casos_edad.csv</i>: Casos diarios en cada rango de edad</li>
        <li> <i>datos_CV_fallecidos_edad.csv</i>: Fallecidos diarios en cada rango de edad</li>
        <li> <i>datos_CV_IA_14d_edad.csv</i>: Incidencia acumulada a 14 días en cada rango de edad. </li>
        <li> <i>datos_CV_IA_14d_sexo.csv</i>: Incidencia acumulada a 14 días para hombres y mujeres. </li>
        <li> <i>datos_CV_por_casos_edad.csv</i>: Porcentaje de casos diarios en cada rango de edad respecto al total de casos diarios.</li>
        <li> <i>datos_CV_por_fallecidos_edad.csv</i>: Porcentaje de fallecidos diarios en cada rango de edad respecto al total de fallecidos diarios.  </li></ul></li>
      <li> <i><b>Covid_CV_Ministerio-script.py</b>:</i> Lee la tabla inicial de los datos diarios del Ministerio para la comunidad de Valencia (<i>COVID_CV_Ministerio.csv</i>) y guardan en una tabla los datos de ingresados en UCI y hospitalizaciones. También se calcula los casos y fallecidos diarios, así como la IA a 14d y 7d, pero no se guardan puesto que no se utilizan. Para la Comunidad de Valencia se usan los datos proporcionados por la Generalitat (parecen más fiables), exceptuando hospitalizaciones y UCI que la GVA no los proporciona. Tabla de salida:
      <ul>
      	<li><i>datos_CV_hosp_UCI.csv</i>: Datos de hospitalizaciones y personas en UCI. Datos totales del día, no los que han ingresado nuevos ese día. </li>
        </ul></li>   
      <li> <b><i>Covid_ESP_Ministerio-script.py</i></b>: Lee la tabla inicial de los datos para España del Ministerio (<i>COVID_CV_Ministerio.csv</i>), se calcula los casos y fallecidos diarios a partir de los totales, se trata los datos, se estima la IA a 14d y 7d, y por último se calcula los casos y fallecidos semanalmente. Todo ello se guarda en diferentes tablas. Los datos se deben tratar por dos motivos: Primero para distribuir los datos entre los fines de semana y festivos como hemos hecho con los datos de la Generalitat. Y segundo, corregir los casos/fallecidos que teníamos como negativos por ajustes que se han hecho en el recuento del Ministerio. En este último caso lo que hacemos es que los 30 días anteriores al valor negativo absorba ese exceso de datos.
      Tablas de salida: 
      <ul>
      <li><i>datos_ESP.csv: Datos diarios de casos y fallecidos durante ese día e incidencia acumulada a 14 días y 7 días. Datos calculados por nosotros y tratados.</i></li>
      <li><i>datos_ESP_hosp_UCI.csv:</i> Datos diarios de hospitalizaciones y hospitalizaciones en UCI. Datos totales del día, no los que han ingresado nuevos ese día. </li>
      <li><i>datos_ESP_sem.csv:</i> Casos y fallecidos acumulados durante 7 días. Datos tratados al igual que los de la tabla datos_ESP.csv y datos calculados por nosotros.</li>
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

Una vez que tenemos la base completa solo con los datos que nos interesa, ya podemos representar los datos y analizarlos. Para ello usamos un notebook de Jupyter en Python (<i>representacion.ipynb</i>). Las gráficas que creamos para analizar los datos son:

<li>Incidencia acumulada a 14 días para la C. Valenciana y España</li>
<li>Incidencia acumulada a 7 días para la C. Valenciana y España</li>
<li>Casos diarios en la C. Valenciana y España: También se muestra la media móvil de los datos usando una ventana de 7 días para poder observar con más claridad la tendencia de los datos.</li>
<li>Casos acumulados en una semana para la C. Valenciana y España</li>
<li>Fallecidos diarios en la C. Valenciana y España: Se muestra también la media móvil con una ventana de 7 días.</li>
<li>Fallecidos acumulados en una semana para la C. Valenciana y España</li>
<li>Hospitalizados e ingresados en UCI en cada momento en la C. Valenciana y España</li>
<li>Gráficas para un análisis más detallado:
	<ul><ul>
		<li>Casos y fallecidos diarios junto con las regiones que hemos utilizado en cada ola y los valores de la letalidad y la mortalidad en cada una de ellas. La letalidad la hemos calculado como el cociente entre los fallecidos y los casos diarios, el valor está dado en porcentaje. La mortalidad se calcula como el cociente entre los fallecidos y la población por cada 100000 habitantes.</li>
		<li>Mapa de calor de la mortalidad para cada ola en la C. Valenciana y España</li>
		<li>Mapa de calor de la letalidad para cada ola en la C. Valenciana y España</li>
		<li>Mortalidad diaria por 100000 habitantes en la C. Valenciana y España. En texto damos también el valor de la mortalidad total</li>
		<li>Media móvil con una ventana de 7 días de los casos y fallecidos diarios, ingresados en UCI y hospitalizados en la C. Valenciana. Se utiliza la media móvil de los casos y los fallecidos porque solo nos interesa la tendencia, además al tener una curva más suavizada se puede mostrar las cuatro curvas en la misma figura y así compararlas. </li>
		<li>Media móvil con una ventana de 7 días de los casos y fallecidos diarios, ingresados en UCI y hospitalizados en España</li>
		<li>Datos normalizados de la media móvil con una ventana de 7 días de los casos y fallecidos diarios, ingresados en UCI y hospitalizados en la C. Valenciana y España. La normalización que usamos es el método de máximo/mínimo. Todos los datos están normalizados, pero la región que usamos para determinar el max/min es desde el principio de la pandemia hasta el 01/12/2020, de tal forma que se queda fuera la expansión de Omicron.</li>
		<li>Incidencia acumulada a 14 días y media móvil con una ventana de 7 días de los fallecidos diarios. De nuevo usamos la media móvil porque solo nos interesa ver la tendencia y así se ve más clara la gráfica.</li>
	</ul></ul></li>
<li> Gráficas de la C. Valenciana con los datos disgregados por rango de edad:
	<ul><ul>
		<li>Media móvil con una ventana de 7 días de los casos diarios para cada rango de edad. Mostramos la media móvil para tener curva más suavizadas y poder mostrar todos los datos juntos y compararlos. Por ello lo usamos en muchas de las siguientes gráficas.</li>
		<li>Media móvil con una ventana de 14 días del porcentaje de los casos diarios en cada rango de edad respecto al total de casos diarios.</li>
		<li>Media móvil con una ventana de 7 días de los fallecidos diarios para cada rango de edad.</li>
		<li>Media móvil con una ventana de 14 días del porcentaje de los fallecidos diarios en cada rango de edad respecto al total de casos diarios.</li>
		<li>Incidencia acumulada a 14 días para rango de edad</li>
		<li>Media móvil con una ventana de 7 días de la mortalidad diaria por rango de edad</li>
		<li>Mapa de calor de la mortalidad para rango de edad y ola</li>
		<li>Mapa de calor de la letalidad para rango de edad y ola</li>
	</ul></ul></li>
<li>Gráficas de la C. Valenciana con los datos disgregados por sexo:
	<ul><ul>
		<li>Casos y fallecidos diarios para hombres y mujeres</li>
		<li>Incidencia acumulada a 14 días para hombres y mujeres</li>
		<li>Media móvil con una ventana de 7 días de la mortalidad diaria para hombres y mujeres. De nuevo volvemos a usar la media móvil para tener una curva más suavizada y poder comparar las dos variables.</li>
		<li>Mapa de calor de la mortalidad para hombres y mujeres en cada ola</li>
		<li>Mapa de calor de la letalidad para hombres y mujeres en cada ola</li>
	</ul></ul></li>







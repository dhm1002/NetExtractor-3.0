![Figura 0](ReadMeImages/NetExtractor2.png)
# Bienvenido a NetExtractor 3.0

NetExtractor 3.0 es un proyecto realizado por la Universidad de Burgos que consiste en una aplicación empleada para generar de forma automática la red de interacciones de personajes en guiones de películas, novelas y obras de teatro con el fin de analizar las redes obtenidas para capturar sus métricas más relevantes.

Las redes van a ser obtenidas mediante:

- La introducción de enlaces a guiones de la página web de https://www.imsdb.com/ en la aplicación.
- La introducción de un fichero tipo ePub para las novelas.
- La selección de corpus y obras de teatro del amplio catálogo de https://dracor.org/.

Una vez que se hayan introducido los requisitos anteriormente mencionados, podremos crear los diccionarios de personajes los cuales podemos modificar, borrar personajes, cambiarlos o combinarlos en caso de que así se requiera. 

Se pueden visualizar las redes de interacción de manera estática y dinámica, para poder ver la evolución de la red en cada instante de tiempo. Una vez generada la red, tendremos un menú de selección de las características deseadas para extraer de la red que, una vez seleccionadas, podrán ser visualizadas en el informe correspondiente. Para las redes dinámicas se puede obtener un informe estático para el instante seleccionado o un informe dinámico, con todas las métricas seleccionadas para varios instantes de tiempo, desde el inicial hasta el actual.

De forma general esto sería lo que hace la aplicación, aun así, en la carpeta "doc" tendremos toda la documentación necesaria así como los manuales de uso de la aplicación.

## Instalación en local:

Para la instalación de todos los componentes necesarios para el despliegue de la aplicación en local, sólo debemos de instalar los componentes necesarios que usaremos que serán los siguientes:

* **Python:** *versión 3.7.4*
* **Flask:** *versión 2.2.2*
* **Flask_Babel:** *versión 1.0.0*
* **numpy:** *versión 1.21.6*
* **matplotlib:** versión *3.5.3*
* **ply:** *versión 3.11*
* **beautifulsoup4:** *versión 4.7.1*
* **lxml:** *versión 4.3.1*
* **html5lib:** *versión 1.0.1*
* **networkx:** *versión 2.4*
* **scipy:** *versión 1.1*
* **DyNetX:** *versión 0.3.1*
* **ffmpeg-python** *versión 0.2.0*
* **IPython** *versión 7.16.3*
* **Werkzeug** *versión 2.2.2*
* **Requests** *versión 2.30.0*
* **gexfpy** *versión 0.1.1*
* **msvc-runtime**: *versión 14.29.30133*

Estos requisitos son de fácil instalación mediante la ejecución del siguiente comando: 

    $ pip install -r requirements.txt

Después simplemente nos moveremos a la carpeta donde tengamos el proyecto y ejecutaremos lo siguiente:

    $ python main.py

Ahora ya tendremos corriendo nuestra aplicación, que se comprueba si en nuestra consola de comandos aparece lo siguiente:

![Figura 1](ReadMeImages/iniciado.PNG)

Finalmente simplemente debemos ir al navegador web que más nos guste e introducir la dirección que aparece en la imagen, es decir http://127.0.0.1:5000 y ya tendríamos nuestra aplicación funcionando en modo local.

## Aplicación desplegada

La aplicación esta abierta y desplegada en https://railway.app/.

Para poder acceder a la aplicación se debe acceder al siguiente link:

https://netextractor3.up.railway.app/

## Uso de la aplicación

A modo de tutorial, se han elaborado dos vídeos con diferentes explicaciones con la finalidad de ayudar al usuario a entender mejor la aplicación. Uno de ellos es una ejecución sencilla de unos cinco minutos, para una obra de teatro. El otro es más extenso, ya que es una ejecución detallada de todas las funcionalidades que contiene la aplicación. 

- Vídeo de la ejecución sencilla:

  https://youtu.be/F1K75OnCqls

- Vídeo de la ejecución completa:

  https://youtu.be/I_fl5TdMJM0

------------------------------------------------------------------------------------------------------------------------------------

# Welcome to NetExtractor 3.0

NetExtractor 3.0 is a University of Burgos's project that consist of an application used to generate automatic character interaction networks of movie scripts, novels and theater plays with the goal of analyze the obtained networks to capture each of its most relevant metrics.

Networks will be obtained through:

- The introduction of links to scripts from the https://www.imsdb.com/ website in the application. 
- The introduction of an ePub type file for the novels.
- The selection of corpora and plays from the extensive catalog of https://dracor.org/.

Once the requirements have been introduced, we can create the character dictionaries which can be modify, delete characters, change them or combine them if required. 

Interaction networks can be visualized statically and dynamically, in order to see the evolution of the network at each instant of time. Once the network is generated, we will have a selection menu of the desired characteristics to extract from the network that, once selected, can be displayed in the corresponding report. For dynamic networks, you can obtain a static report for the selected instant or a dynamic report, with all the metrics selected for various instants of time, from the initial to the current one.

In general, this would be what the application does, even so, in this repository we have all the information about the project, in the "doc" folder we will have all the necessary documentation as well as the application usage manuals.

## Local instalation:

For the installation of all the necessary components for the deployment of the application locally, we only have to install the necessary components that we will use which will be the following:

* **Python:** *version 3.7.4*
* **Flask:** *version 2.2.2*
* **Flask_Babel:** *version 1.0.0*
* **numpy:** *version 1.21.6*
* **matplotlib:** version *3.5.3*
* **ply:** *version 3.11*
* **beautifulsoup4:** *version 4.7.1*
* **lxml:** *version 4.3.1*
* **html5lib:** *version 1.0.1*
* **networkx:** *version 2.4*
* **scipy:** *version 1.1*
* **DyNetX:** *version 0.3.1*
* **ffmpeg-python** *version 0.2.0*
* **IPython** *version 7.16.3*
* **Werkzeug** *version 2.2.2*
* **Requests** *version 2.30.0*
* **gexfpy** *version 0.1.1*
* **msvc-runtime**: *version 14.29.30133*

These requirements are easy to install by executing the following command:

    $ pip install -r requirements.txt

Then we will simply move to the folder where we have the project and execute the following:

    $ python main.py

Now we will have our application running, which checks if the following appears in our command console:

![Figure 1](ReadMeImages/iniciado.PNG)

Finally we simply have to go to the web browser that we like the most and enter the address that appears in the image, that is http://127.0.0.1:5000 and we would already have our application running locally.

## Deployed application

The application is open and deployed in https://railway.app/.

To access the application you must access the following link:

https://netextractor3.up.railway.app/
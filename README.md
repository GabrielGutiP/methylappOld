# MethylApp (OLD)
Final Project for Software Engineering Degree. Web tool used to find patterns in baterian methylations.
This project is deprecated and a new version can be found in [MethylApp](https://github.com/GabrielGutiP/methylapp).

To install follow these steps:
1. Intall Python. If you don't have one installed, it is recommended version 3.9.5 as the project was made with it. Here you could download the version you wish: https://www.python.org/downloads/windows/.

2. Create a virtual enviroment. The folder where you created doesn't matter. Then use this command:
	
	python -m venv nombreEnv

3. Virtual enviroment, To work with it, you must be at the same folder where you created it and use this command:
	
	nombreEnv\Scripts\activate

Now we are in the virtual enviroment which we'll let us make an isoleted instalation of all requirements.

4. Install requirements. Unzip the downloaded "methylapp.zip". Move to the folder where you unziped it and use the next command:

	pip install -r requirements.txt

5. Use this command to run the application while being on the same folder level as before:
	
	python manage.py runserver

6. Visualize the lunched app. Go to this direction in your browser: http://127.0.0.1:8000/

# MethylApp (Antiguo)
Trabajo de Fin de Grado. Desarrollo de una herramienta web para el apoyo en el análisis de las metilaciones bacterianas.

Para intalar código seguir los siguientes pasos:
1. Instalar Python. Si no se tiene instalado, es recomendable la descarga de la versión 3.9.5 que ha sido la usada para este proyecto. Aquí podrá descargar la versión para Windows que desee: https://www.python.org/downloads/windows/.

2. Crear un entorno virtual. La carpeta donde se creé no importa. Después usamos el siguiente comando:
	
	python -m venv nombreEnv

3. Trabajar con el entorno virtual. Para trabajar con el entono virtual, estado a la altura donde lo haya creado, realizar el siguiente comando:
	
	nombreEnv\Scripts\activate

Ahora estamos dentro del entono virtual, que nos permitirá realizar una instalación aislada de todos los requerimientos.

4. Instalamos los requerimientos. Para ello descomprimimos el zip donde está la aplicación, “methylapp.zip”, en la carpeta que queramos. Una vez hecho, navegamos a la carpeta que contiene el archivo “requirements.txt” con los comandos necesarios y luego realizamos la instalación de la siguiente manera:
Tras esto aparecerán todo lo necesario para el despliegue del sistema, esperamos a que la instalación acabe.

	pip install -r requirements.txt

5. Lanzamiento de la aplicación. Nos mantenemos al mismo nivel que antes y ejecutamos el siguiente comando:
	
	python manage.py runserver

6. Visualizar el despliegue. Para ver lo que hemos desplegado nos dirigimos a la siguiente dirección en un navegador web: http://127.0.0.1:8000/.

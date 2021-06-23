# MethylApp
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

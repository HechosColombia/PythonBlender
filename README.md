Visualización de Datos Dinámica de Población en Blender con Python
Esta aplicación Python utiliza Blender para crear una visualización dinámica de la evolución de la población de diferentes comunas a lo largo del tiempo, basada en datos de un archivo CSV. Cada comuna es representada por una barra 3D que se eleva y se reduce en función de su población en cada año, creando una animación visualmente impactante.
Para generar las formas de cada comuna en Blender, se utilizó un shapefile descargado previamente desde QGIS. Este archivo vectorial contiene la geometría precisa de cada comuna, lo que permite una representación geográfica precisa en la visualización. Al importar el shapefile a Blender, se crean objetos 3D que se utilizan como base para las barras que representan la población de cada comuna. Esto garantiza que la visualización no solo sea estéticamente atractiva, sino también geográficamente correcta
Características Clave
Importación de datos CSV: Carga datos de población desde un archivo CSV con estructura flexible.
Generación de barras 3D: Crea barras 3D en Blender para representar cada comuna.
Animación: Anima las barras para mostrar la evolución de la población a lo largo de los años.
Etiquetas y líneas: Incluye etiquetas de texto con el nombre de la comuna y su población, conectadas a las barras mediante líneas.
Personalización: Permite ajustar los colores, el rango de años y otros parámetros.
Requisitos Previos
Blender: Versión 2.93 o superior.
Python: Versión 3.x con las siguientes librerías:
bpy: Para interactuar con Blender.
pandas: Para procesar los datos del CSV.
Estructura del Proyecto
main.py: Contiene el código principal de la aplicación.
data/: Carpeta para almacenar los archivos CSV con los datos de población.
Instalación y Uso
Clonar el repositorio:
git clone (https://github.com/HechosColombia/PythonBlender)
Preparar el archivo CSV:
Asegúrate de que tu archivo CSV tenga las siguientes columnas (ajustables en el código):
numero: Identificador único de la comuna.
nombre_comuna: Nombre de la comuna.
Columnas numéricas para cada año (por ejemplo, 2018, 2019, ...).
Guarda el archivo CSV en la carpeta data/.
Ejecutar el script:
Abre el archivo .blend correspondiente en Blender.
Ejecuta el script main.py desde la consola de Python de Blender.
Personalización
Colores: Modifica los valores de random.random() en la función crear_barras() para personalizar los colores de las barras.
Rango de años: Ajusta el rango de años en los bucles for de las funciones crear_barras() y crear_etiqueta_texto().
Otras opciones: Explora el código para encontrar más opciones de personalización.
Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue en GitHub para discutir cualquier cambio o mejora.

Licencia
Este proyecto está bajo la licencia MIT.

Ejemplo de Archivo CSV

![image](https://github.com/user-attachments/assets/8ddb8d9b-20fb-4d7d-8424-501573623398)



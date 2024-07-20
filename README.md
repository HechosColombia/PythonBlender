### This readme is in english and in the lower part is in spanish
### Este readme esta en ingles y en la parte de abajo en español
# ENGLISH
# SpotifyBlender
## Music Listening Data Visualization in Blender

### Introduction

This Python script uses Blender and pandas to create a visual animation of music listening data contained in a JSON file. The animation shows how the ranking of the top 10 most listened artists evolves over time.

### Requirements

* Blender
* Python with the following libraries:
    * pandas
    * numpy

### Usage

1. **Setup:**
   * **JSON File:** Modify the `json_file_path` variable to point to your JSON file with listening data.
   * **Date Range:** Adjust the start date if you want to analyze a different period.

2. **Run:**
   * Open the .blend file in Blender.
   * Run the script from Blender's Python console.

### Customization

* **Artists:** You can change the number of artists to visualize.
* **Colors:** Customize the colors of the bars and text.
* **Visual Effects:** Experiment with different visual effects (e.g., particles, lights).

### Visualization

The resulting animation shows bars representing the top 10 most listened artists. The height of each bar indicates the total number of hours the artist has been listened to up to that date. Additional text displays the date corresponding to each frame.

### Code Structure

* **Data Loading:** Loads the data from the JSON file and processes it to get the top 10 artists and dates.
* **Object Creation:** Creates Blender objects (bars, text) to represent the data.
* **Animation:** Creates keyframes to animate the bars and text over time.

### Contributions

Contributions are welcome. Please open an issue or a pull request on GitHub.

### License

This project is licensed under the MIT license.

---

# MAPASBLENDER.PY CODE

## Dynamic Population Data Visualization in Blender with Python

This Python application uses Blender to create a dynamic visualization of the population evolution of different communes over time, based on data from a CSV file. Each commune is represented by a 3D bar that rises and falls based on its population in each year, creating a visually striking animation.

To generate the shapes of each commune in Blender, a shapefile previously downloaded from QGIS was used. This vector file contains the precise geometry of each commune, allowing for an accurate geographical representation in the visualization. By importing the shapefile into Blender, 3D objects are created that serve as the base for the bars representing each commune's population. This ensures that the visualization is not only aesthetically pleasing but also geographically accurate.

### Key Features

- **CSV Data Import:** Loads population data from a CSV file with a flexible structure.
- **3D Bar Generation:** Creates 3D bars in Blender to represent each commune.
- **Animation:** Animates the bars to show the population evolution over the years.
- **Labels and Lines:** Includes text labels with the commune's name and population, connected to the bars by lines.
- **Customization:** Allows for adjusting colors, year range, and other parameters.

### Prerequisites

- **Blender:** Version 2.93 or higher.
- **Python:** Version 3.x with the following libraries:
  - `bpy`: To interact with Blender.
  - `pandas`: To process the CSV data.

### Project Structure

- `main.py`: Contains the main application code.
- `data/`: Folder to store the CSV files with population data.

### Installation and Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HechosColombia/PythonBlender
### CSV File Preparation:

Ensure your CSV file has the following columns (adjustable in the code):

* **numero:** Unique identifier of the commune.
* **nombre_comuna:** Name of the commune.
* Numeric columns for each year (e.g., 2018, 2019, ...).

Save the CSV file in the `data/` folder.

### Run the script:

1. **Open the corresponding .blend file in Blender.**
2. **Run the `main.py` script from Blender's Python console.**

### Customization

* **Colors:** Modify the `random.random()` values in the `crear_barras()` function to customize the colors of the bars.
* **Year Range:** Adjust the year range in the `for` loops of the `crear_barras()` and `crear_etiqueta_texto()` functions.
* **Other Options:** Explore the code to find more customization options.

### Contributions

Contributions are welcome. Please open an issue on GitHub to discuss any changes or improvements.

### License

This project is under the MIT license.

### Example CSV File
![image](https://github.com/user-attachments/assets/8ddb8d9b-20fb-4d7d-8424-501573623398)


# ESPAÑOL

SpotifyBlender
# Visualización de datos de escucha musical en Blender

## Introducción

Este script de Python utiliza Blender y pandas para crear una animación visual de los datos de escucha musical contenidos en un archivo JSON. La animación muestra cómo evoluciona el ranking de los 10 artistas más escuchados a lo largo del tiempo.

## Requisitos

* Blender
* Python con las siguientes bibliotecas:
    * pandas
    * numpy

## Uso

1. **Configurar:**
   * **Archivo JSON:** Modifica la variable `json_file_path` para apuntar al archivo JSON con tus datos de escucha.
   * **Rango de fechas:** Ajusta la fecha de inicio si deseas analizar un período diferente.

2. **Ejecutar:**
   * Abre el archivo .blend en Blender.
   * Ejecuta el script desde la consola de Python de Blender.

## Personalización

* **Artistas:** Puedes modificar el número de artistas a visualizar.
* **Colores:** Personaliza los colores de las barras y el texto.
* **Efectos visuales:** Experimenta con diferentes efectos visuales (e.g., partículas, luces).

## Visualización

La animación resultante muestra barras que representan a los 10 artistas más escuchados. La altura de cada barra indica el número total de horas que se ha escuchado al artista hasta esa fecha. Un texto adicional muestra la fecha correspondiente a cada frame.

## Estructura del código

* **Carga de datos:** Carga los datos del archivo JSON y los procesa para obtener los 10 artistas principales y las fechas.
* **Creación de objetos:** Crea objetos de Blender (barras, texto) para representar los datos.
* **Animación:** Crea keyframes para animar las barras y el texto a lo largo del tiempo.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request en GitHub.

## Licencia

Este proyecto está licenciado bajo la licencia MIT.



MAPASBLENDER.PY CODE:

# Visualización de Datos Dinámica de Población en Blender con Python

Esta aplicación Python utiliza Blender para crear una visualización dinámica de la evolución de la población de diferentes comunas a lo largo del tiempo, basada en datos de un archivo CSV. Cada comuna es representada por una barra 3D que se eleva y se reduce en función de su población en cada año, creando una animación visualmente impactante.

Para generar las formas de cada comuna en Blender, se utilizó un shapefile descargado previamente desde QGIS. Este archivo vectorial contiene la geometría precisa de cada comuna, lo que permite una representación geográfica precisa en la visualización. Al importar el shapefile a Blender, se crean objetos 3D que se utilizan como base para las barras que representan la población de cada comuna. Esto garantiza que la visualización no solo sea estéticamente atractiva, sino también geográficamente correcta.

## Características Clave

- **Importación de datos CSV**: Carga datos de población desde un archivo CSV con estructura flexible.
- **Generación de barras 3D**: Crea barras 3D en Blender para representar cada comuna.
- **Animación**: Anima las barras para mostrar la evolución de la población a lo largo de los años.
- **Etiquetas y líneas**: Incluye etiquetas de texto con el nombre de la comuna y su población, conectadas a las barras mediante líneas.
- **Personalización**: Permite ajustar los colores, el rango de años y otros parámetros.

## Requisitos Previos

- **Blender**: Versión 2.93 o superior.
- **Python**: Versión 3.x con las siguientes librerías:
  - `bpy`: Para interactuar con Blender.
  - `pandas`: Para procesar los datos del CSV.

## Estructura del Proyecto

- `main.py`: Contiene el código principal de la aplicación.
- `data/`: Carpeta para almacenar los archivos CSV con los datos de población.

## Instalación y Uso

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/HechosColombia/PythonBlender
### Preparación del archivo CSV:

Asegúrate de que tu archivo CSV tenga las siguientes columnas (ajustables en el código):

* **numero:** Identificador único de la comuna.
* **nombre_comuna:** Nombre de la comuna.
* Columnas numéricas para cada año (por ejemplo, 2018, 2019, ...).

Guarda el archivo CSV en la carpeta `data/`.

### Ejecutar el script:

1. **Abre el archivo .blend correspondiente en Blender.**
2. **Ejecuta el script `main.py` desde la consola de Python de Blender.**

### Personalización

* **Colores:** Modifica los valores de `random.random()` en la función `crear_barras()` para personalizar los colores de las barras.
* **Rango de años:** Ajusta el rango de años en los bucles `for` de las funciones `crear_barras()` y `crear_etiqueta_texto()`.
* **Otras opciones:** Explora el código para encontrar más opciones de personalización.

### Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue en GitHub para discutir cualquier cambio o mejora.

### Licencia

Este proyecto está bajo la licencia MIT.


# Ejemplo de Archivo CSV

![image](https://github.com/user-attachments/assets/8ddb8d9b-20fb-4d7d-8424-501573623398)



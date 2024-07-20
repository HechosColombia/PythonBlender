import bpy
import pandas as pd

# Set the appropriate context by selecting a scene / Establecer el contexto adecuado seleccionando una escena
bpy.context.view_layer.objects.active = bpy.context.view_layer.objects[0]

# Delete existing objects in the scene if any / Eliminar los objetos existentes en la escena si los hay
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Delete all text objects in the scene / Eliminar todos los textos en la escena
bpy.ops.object.select_by_type(type='FONT')
bpy.ops.object.delete()

# Path to the JSON file / Ruta del archivo JSON
json_file_path = "C:\\Users\\usuario\\StreamingHistory0.json"

# Load the data from the JSON file / Cargar los datos desde el archivo JSON
df = pd.read_json(json_file_path)

# Filter the base to get only the top 10 artists based on total hours played / Filtrar la base para obtener solo los 10 principales artistas según el total de horas reproducidas
top_10_artists = df.groupby('artistName')['msPlayed'].sum().nlargest(10).index
df = df[df['artistName'].isin(top_10_artists)]

# Convert the 'endTime' column to datetime format / Convertir la columna 'endTime' al formato de fecha y hora
df['endTime'] = pd.to_datetime(df['endTime'])

# Get unique dates for keyframes / Obtener las fechas únicas para las keyframes
unique_dates = sorted(df['endTime'].dt.date.unique())

# Find the index of the date 2023-02-01 / Encontrar el índice de la fecha 2023-02-01
start_index = unique_dates.index(pd.Timestamp('2023-02-01').date())

# Reorder the list of dates to start with 2023-02-01 / Reordenar la lista de fechas para que comience con 2023-02-01
unique_dates = unique_dates[start_index:] + unique_dates[:start_index]

# Variable for X-axis offset / Variable para el desplazamiento en el eje X
x_offset = 0

# Get the top 10 artists in February 2023 / Obtener los 10 principales artistas en febrero de 2023
feb_01_2023_data = df[df['endTime'].dt.date == pd.Timestamp('2023-02-01').date()]
artist_hours_feb_01_2023 = feb_01_2023_data.groupby('artistName')['msPlayed'].sum() / (1000 * 60 * 60)  # Convert ms to hours / Convertir ms a horas
top_artists_feb_01_2023 = artist_hours_feb_01_2023.nlargest(10)
ordered_artists = top_artists_feb_01_2023.index

# Create initial bars to represent the top artists / Crear barras iniciales para representar a los artistas principales
bars = []  # List to store the created bars / Lista para almacenar las barras creadas
for artist_name in top_10_artists:
    hours_played = artist_hours_feb_01_2023.get(artist_name, 0)  # Get the hours played for the artist / Obtener las horas reproducidas para el artista
    # Create a bar / Crear una barra
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x_offset, 0, hours_played / 2))  # Initial position on Z-axis / Posición inicial en el eje Z
    bar = bpy.context.active_object
    bar.scale = (1, 1, hours_played)  # Adjust height based on hours played / Ajustar altura según las horas reproducidas
    
    # Create a new blue metallic material / Crear un nuevo material azul metalizado
    mat = bpy.data.materials.new(name="BlueMetallic")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    principled_bsdf = nodes.get("Principled BSDF")
    principled_bsdf.inputs[0].default_value = (0.0, 0.5, 1.0, 1.0)  # Blue color / Color azul
    principled_bsdf.inputs[7].default_value = 0.5  # Metallic value / Valor de metalidad
    bar.data.materials.append(mat)  # Assign the material to the bar / Asignar el material a la barra
    
    bar.name = artist_name  # Assign the artist's name to the bar / Asignar el nombre del artista a la barra
    bars.append(bar)  # Add the bar to the list / Agregar la barra a la lista
    x_offset += 2  # Increment the X-axis offset for the next bar / Incrementar el desplazamiento en el eje X para la siguiente barra

# Create keyframes to animate the chart / Crear keyframes para animar la gráfica
scene = bpy.context.scene

# Set the first frame as the start of the animation (February 1, 2023) / Establecer el primer frame como inicio de la animación (01 de febrero de 2023)
scene.frame_set(1)

# Create a keyframe for each bar at the first frame (February 1, 2023) / Crear un keyframe para cada barra en el primer frame (01 de febrero de 2023)
for bar in bars:
    bar.keyframe_insert(data_path="scale", index=2)  # Create a keyframe for the scale on the Z-axis of the bar / Crear un keyframe para la escala en el eje Z de la barra
    bar.keyframe_insert(data_path="location", index=2)  # Create a keyframe for the location of the bar / Crear un keyframe para la ubicación de la barra

# Get cumulative data from February 1, 2023 / Obtener los datos acumulados desde el 01 de febrero de 2023
cumulative_hours = artist_hours_feb_01_2023.copy()

# Update the bars for each keyframe from February 1, 2023 / Actualizar las barras para cada keyframe desde el 01 de febrero de 2023
for i, date in enumerate(unique_dates[1:], start=2):  # Start from the second frame / Comenzar desde el segundo frame
    scene.frame_set(i)
    current_date_data = df[df['endTime'].dt.date == date]
    monthly_hours = current_date_data.groupby('artistName')['msPlayed'].sum() / (1000 * 60 * 60)
    cumulative_hours = cumulative_hours.add(monthly_hours, fill_value=0)
    for artist_name, bar in zip(top_10_artists, bars):
        hours_played = cumulative_hours.get(artist_name, 0)
        new_scale_z = hours_played if hours_played > 0 else 0.0001  # Symbolic value if no data for this date / Valor simbólico si no hay datos para esta fecha
        height_diff = new_scale_z - bar.scale.z
        bar.scale.z = new_scale_z
        bar.location.z += height_diff / 2
        bar.keyframe_insert(data_path="scale", index=2)
        bar.keyframe_insert(data_path="location", index=2)

# Set the first frame as the start of the animation / Establecer el primer frame como inicio de la animación
scene.frame_set(1)

# Get the top 10 artists based on total hours played (before filtering by February 2023) / Obtener los 10 principales artistas basados en el total de horas reproducidas (antes de filtrar por febrero de 2023)
top_10_artists_original_order = df.groupby('artistName')['msPlayed'].sum().nlargest(10).index

# Store the original order of artists before filtering / Almacenar el orden original de los artistas antes del filtrado
original_order_dict = {artist: idx for idx, artist in enumerate(top_10_artists_original_order)}

# Filter the data to start from February 2023 / Filtrar los datos para comenzar desde febrero de 2023
start_date = pd.Timestamp('2023-02-01')
df = df[df['endTime'] >= start_date]

# Get unique dates for keyframes / Obtener las fechas únicas para las keyframes
unique_dates = sorted(df['endTime'].dt.date.unique())

# Create a dictionary to store accumulated hours per day for the top 10 artists / Crear un diccionario para almacenar las horas acumuladas por día para los 10 principales artistas
cumulative_hours = {artist: [] for artist in top_10_artists_original_order}

# Calculate accumulated hours per day for each artist / Calcular las horas acumuladas por día para cada artista
for date in unique_dates:
    daily_data = df[df['endTime'].dt.date == date]
    artist_hours = daily_data.groupby('artistName')['msPlayed'].sum() / (1000 * 60 * 60)  # Convert ms to hours / Convertir ms a horas
    for artist in top_10_artists_original_order:
        if artist in artist_hours:
            if date == unique_dates[0]:
                cumulative_hours[artist].append(artist_hours[artist])
            else:
                cumulative_hours[artist].append(artist_hours[artist] + cumulative_hours[artist][-1])
        else:
            if date == unique_dates[0]:
                cumulative_hours[artist].append(0)
            else:
                cumulative_hours[artist].append(cumulative_hours[artist][-1])

# Function to update text objects with accumulated hours per day for the top 10 artists / Función para actualizar los objetos de texto con las horas acumuladas por día para los 10 principales artistas
def update_text_objects(scene):
    current_frame = scene.frame_current
    if current_frame in cumulative_keyframes:
        daily_hours = cumulative_keyframes[current_frame]
        for artist in top_10_artists_original_order:
            idx = original_order_dict[artist]
            if len(daily_hours[artist]) > 0:
                text_objects[idx].data.body = f"{artist}: {daily_hours[artist][-1]:.2f} horas"

# Create a dictionary to store accumulated hours per day for each artist at each keyframe / Crear un diccionario para almacenar las horas acumuladas por día para cada artista en cada keyframe
cumulative_keyframes = {}

# Assign accumulated hours per day to the keyframes dictionary / Asignar las horas acumuladas por día al diccionario de keyframes
for i, date in enumerate(unique_dates):
    frame = i + 1
    cumulative_keyframes[frame] = {artist: [cumulative_hours[artist][i]] for artist in top_10_artists_original_order}

# Initialize x_offset at 0 / Inicializar x_offset en 0
x_offset = 0.3

# Create and position text objects to show accumulated hours per day for the top 10 artists / Crear y posicionar los objetos de texto para mostrar las horas acumuladas por día para los 10 principales artistas
text_objects = []
for artist_name in top_10_artists_original_order:  # Use original order before filtering by February 2023 / Usar el orden original antes de filtrar por febrero de 2023
    # Create a text object / Crear un objeto de texto
    text_object = bpy.data.objects.new("Text", bpy.data.curves.new(name="Curve", type='FONT'))
    text_object.location = (x_offset, -0.5, 0)
    text_object.rotation_euler = (1.5708, -1.5708, 0)  # Rotate the text 90 degrees around the X-axis / Rotar el texto 90 grados alrededor del eje X
    text_object.data.extrude = 0.1  # Adjust text thickness / Ajustar el grosor del texto
    
    # Configure the text material / Configurar el material del texto
    mat = bpy.data.materials.new(name="BlackText")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    diffuse_shader = nodes.get("Principled BSDF")
    diffuse_shader.inputs[0].default_value = (0, 0, 0, 1)  # Black color / Color negro
    text_object.data.materials.append(mat)  # Assign the material to the text object / Asignar el material al objeto de texto

    bpy.context.collection.objects.link(text_object)
    text_objects.append(text_object)
    x_offset += 2  # Increment the X-axis offset for the next text / Incrementar el desplazamiento en el eje X para el siguiente texto

# Register the update function for each frame change / Registrar la función de actualización para cada cambio de frame
bpy.app.handlers.frame_change_pre.append(update_text_objects)

# Set the first frame as the start of the animation / Establecer el primer frame como inicio de la animación
bpy.context.scene.frame_set(1)

# Create a text object for dates / Crear un objeto de texto para las fechas
bpy.ops.object.text_add(location=(-1, 0, -5))
date_text = bpy.context.object
date_text.data.body = ""  # Initially empty / Inicialmente vacío
date_text.rotation_euler = (1.5708, 0, 0)
date_text.data.size = 5.0  # Change 2.0 to the desired size / Cambia 2.0 al tamaño que desees

# Create a new black material / Crear un nuevo material negro
mat = bpy.data.materials.new(name="Black")
mat.diffuse_color = (0, 0, 0, 1)  # Set material color to black / Establecer el color del material a negro

# Assign the material to the text object / Asignar el material al objeto de texto
if date_text.data.materials:
    date_text.data.materials[0] = mat
else:
    date_text.data.materials.append(mat)

# Function to update the text with the date on each frame change / Función para actualizar el texto con la fecha en cada cambio de frame
def update_date_text(scene):
    current_frame = scene.frame_current
    if current_frame in text_keyframes:
        date = text_keyframes[current_frame]
        date_text.data.body = date

# Create a dictionary to store text assignments to keyframes / Crear un diccionario para almacenar las asignaciones de texto a keyframe
text_keyframes = {}

# Create keyframes to show the corresponding dates / Crear keyframes para mostrar las fechas correspondientes
for i, date in enumerate(unique_dates):
    frame = i + 1
    text_keyframes[frame] = str(date)

# Register the update function for each frame change / Registrar la función de actualización para cada cambio de frame
bpy.app.handlers.frame_change_pre.append(update_date_text)

# Set the first frame as the start of the animation / Establecer el primer frame como inicio de la animación
bpy.context.scene.frame_set(1)

# Create a text object / Crear un objeto de texto
bpy.ops.object.text_add(location=(-3, 0, 0))
text_object = bpy.context.object
text_object.data.body = "Horas escuchadas"
text_object.data.extrude = 0.1
text_object.data.bevel_depth = 0.02
text_object.data.size = 4

# Configure the text material / Configurar el material del texto
material = bpy.data.materials.new(name="BlueMaterial")
material.diffuse_color = (0, 0, 1, 1)  # Blue color (RGBA) / Color azul (RGBA)
text_object.data.materials.append(material)

# Rotate the text to be horizontal and parallel to the X-axis / Rotar el texto para que esté horizontal y paralelo al eje X
text_object.rotation_euler = (1.5708, -1.5708, 0)

# Create a text object / Crear un objeto de texto
bpy.ops.object.text_add(location=(-8, 0, 36))
text_object = bpy.context.object
text_object.data.body = "Top 10 Artistas"
text_object.data.extrude = 0.1
text_object.data.bevel_depth = 0.02
text_object.data.size = 4

# Configure the text material / Configurar el material del texto
material = bpy.data.materials.new(name="BlueMaterial")
material.diffuse_color = (0, 0, 1, 1)  # Blue color (RGBA) / Color azul (RGBA)
text_object.data.materials.append(material)

# Rotate the text to be horizontal and parallel to the X-axis / Rotar el texto para que esté horizontal y paralelo al eje X
text_object.rotation_euler = (1.5708, 0, 0)

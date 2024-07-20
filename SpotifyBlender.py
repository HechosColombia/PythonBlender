import bpy
import pandas as pd

# Establecer el contexto adecuado seleccionando una escena
bpy.context.view_layer.objects.active = bpy.context.view_layer.objects[0]

# Eliminar los objetos existentes en la escena si los hay
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Eliminar todos los textos en la escena
bpy.ops.object.select_by_type(type='FONT')
bpy.ops.object.delete()

# Ruta del archivo JSON
json_file_path = "C:\\Users\\usuario\StreamingHistory0.json"

# Cargar los datos desde el archivo JSON
df = pd.read_json(json_file_path)

# Filtrar la base para obtener solo los 10 principales artistas según el total de horas reproducidas
top_10_artists = df.groupby('artistName')['msPlayed'].sum().nlargest(10).index
df = df[df['artistName'].isin(top_10_artists)]

# Convertir la columna 'endTime' al formato de fecha y hora
df['endTime'] = pd.to_datetime(df['endTime'])

# Obtener las fechas únicas para las keyframes
unique_dates = sorted(df['endTime'].dt.date.unique())

# Encontrar el índice de la fecha 2023-02-01
start_index = unique_dates.index(pd.Timestamp('2023-02-01').date())

# Reordenar la lista de fechas para que comience con 2023-02-01
unique_dates = unique_dates[start_index:] + unique_dates[:start_index]

# Variable para el desplazamiento en el eje X
x_offset = 0

# Obtener los 10 principales artistas en febrero de 2023
feb_01_2023_data = df[df['endTime'].dt.date == pd.Timestamp('2023-02-01').date()]
artist_hours_feb_01_2023 = feb_01_2023_data.groupby('artistName')['msPlayed'].sum() / (1000 * 60 * 60)  # Convertir ms a horas
top_artists_feb_01_2023 = artist_hours_feb_01_2023.nlargest(10)
ordered_artists = top_artists_feb_01_2023.index

# Crear barras iniciales para representar a los artistas principales
bars = []  # Lista para almacenar las barras creadas
for artist_name in top_10_artists:
    hours_played = artist_hours_feb_01_2023.get(artist_name, 0)  # Obtener las horas reproducidas para el artista
    # Crear una barra
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x_offset, 0, hours_played / 2))  # Posición inicial en el eje Z
    bar = bpy.context.active_object
    bar.scale = (1, 1, hours_played)  # Ajustar la altura según las horas reproducidas
    
    # Crear un nuevo material azul metalizado
    mat = bpy.data.materials.new(name="BlueMetallic")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    principled_bsdf = nodes.get("Principled BSDF")
    principled_bsdf.inputs[0].default_value = (0.0, 0.5, 1.0, 1.0)  # Color azul
    principled_bsdf.inputs[7].default_value = 0.5  # Valor de metalidad
    bar.data.materials.append(mat)  # Asignar el material a la barra
    
    bar.name = artist_name  # Asignar el nombre del artista a la barra
    bars.append(bar)  # Agregar la barra a la lista
    x_offset += 2  # Incrementar el desplazamiento en el eje X para la próxima barra

# Crear keyframes para animar la gráfica
scene = bpy.context.scene

# Establecer el primer frame como inicio de la animación (01 de febrero de 2023)
scene.frame_set(1)

# Crear un keyframe para cada barra en el primer frame (01 de febrero de 2023)
for bar in bars:
    bar.keyframe_insert(data_path="scale", index=2)  # Crear un keyframe para la escala en el eje Z de la barra
    bar.keyframe_insert(data_path="location", index=2)  # Crear un keyframe para la ubicación de la barra

# Obtener los datos acumulados desde el 01 de febrero de 2023
cumulative_hours = artist_hours_feb_01_2023.copy()

# Actualizar las barras para cada keyframe desde el 01 de febrero de 2023
for i, date in enumerate(unique_dates[1:], start=2):  # Comenzar desde el segundo frame
    scene.frame_set(i)
    current_date_data = df[df['endTime'].dt.date == date]
    monthly_hours = current_date_data.groupby('artistName')['msPlayed'].sum() / (1000 * 60 * 60)
    cumulative_hours = cumulative_hours.add(monthly_hours, fill_value=0)
    for artist_name, bar in zip(top_10_artists, bars):
        hours_played = cumulative_hours.get(artist_name, 0)
        new_scale_z = hours_played if hours_played > 0 else 0.0001  # Valor simbólico si no hay datos para esta fecha
        height_diff = new_scale_z - bar.scale.z
        bar.scale.z = new_scale_z
        bar.location.z += height_diff / 2
        bar.keyframe_insert(data_path="scale", index=2)
        bar.keyframe_insert(data_path="location", index=2)

# Establecer el primer frame como inicio de la animación
scene.frame_set(1)







# Obtener los 10 principales artistas basados en el total de horas reproducidas (antes de filtrar por febrero de 2023)
top_10_artists_original_order = df.groupby('artistName')['msPlayed'].sum().nlargest(10).index

# Almacenar el orden original de los artistas antes del filtrado
original_order_dict = {artist: idx for idx, artist in enumerate(top_10_artists_original_order)}

# Filtrar los datos para comenzar desde febrero de 2023
start_date = pd.Timestamp('2023-02-01')
df = df[df['endTime'] >= start_date]

# Obtener las fechas únicas para las keyframes
unique_dates = sorted(df['endTime'].dt.date.unique())

# Crear un diccionario para almacenar las horas acumuladas por día para los 10 principales artistas
cumulative_hours = {artist: [] for artist in top_10_artists_original_order}

# Calcular las horas acumuladas por día para cada artista
for date in unique_dates:
    daily_data = df[df['endTime'].dt.date == date]
    artist_hours = daily_data.groupby('artistName')['msPlayed'].sum() / (1000 * 60 * 60)  # Convertir ms a horas
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

# Función para actualizar los objetos de texto con los valores acumulados por día para los 10 principales artistas
def update_text_objects(scene):
    current_frame = scene.frame_current
    if current_frame in cumulative_keyframes:
        daily_hours = cumulative_keyframes[current_frame]
        for artist in top_10_artists_original_order:
            idx = original_order_dict[artist]
            if len(daily_hours[artist]) > 0:
                text_objects[idx].data.body = f"{artist}: {daily_hours[artist][-1]:.2f} horas"

# Crear un diccionario para almacenar las horas acumuladas por día para cada artista en cada keyframe
cumulative_keyframes = {}

# Asignar las horas acumuladas por día al diccionario de keyframes
for i, date in enumerate(unique_dates):
    frame = i + 1
    cumulative_keyframes[frame] = {artist: [cumulative_hours[artist][i]] for artist in top_10_artists_original_order}
    
# Inicializar x_offset en 0
x_offset = 0.3
# Crear y posicionar los objetos de texto para mostrar las horas acumuladas por día para los 10 principales artistas
text_objects = []
for artist_name in top_10_artists_original_order:  # Usar el orden original antes de filtrar por febrero de 2023
    text_object = bpy.data.objects.new("Text", bpy.data.curves.new(name="Curve", type='FONT'))
    text_object.location = (x_offset, -0.5, 0)
    text_object.rotation_euler = (1.5708, -1.5708, 0)  # Rotar el texto 90 grados alrededor del eje X
    text_object.data.extrude = 0.1  # Ajustar el grosor del texto
    
    # Configurar el material del texto
    mat = bpy.data.materials.new(name="BlackText")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    diffuse_shader = nodes.get("Principled BSDF")
    diffuse_shader.inputs[0].default_value = (0, 0, 0, 1)  # Color negro
    text_object.data.materials.append(mat)  # Asignar el material al objeto de texto

    
    bpy.context.collection.objects.link(text_object)
    text_objects.append(text_object)
    x_offset += 2  # Incrementar el desplazamiento en el eje X para el próximo texto


# Registrar la función de actualización para cada cambio de frame
bpy.app.handlers.frame_change_pre.append(update_text_objects)

# Establecer el primer frame como inicio de la animación
bpy.context.scene.frame_set(1)


# Crea un objeto de texto para las fechas
bpy.ops.object.text_add(location=(-1, 0, -5))
date_text = bpy.context.object
date_text.data.body = ""  # Inicialmente vacío
date_text.rotation_euler = (1.5708, 0, 0)
# Ajusta el tamaño del texto
date_text.data.size = 5.0  # Cambia 2.0 al tamaño que desees
# Crea un nuevo material negro
mat = bpy.data.materials.new(name="Black")
mat.diffuse_color = (0, 0, 0, 1)  # Establece el color del material a negro

# Asigna el material al objeto de texto
if date_text.data.materials:
    date_text.data.materials[0] = mat
else:
    date_text.data.materials.append(mat)

# Función para actualizar el texto en cada cambio de frame
def update_date_text(scene):
    current_frame = scene.frame_current
    if current_frame in text_keyframes:
        date = text_keyframes[current_frame]
        date_text.data.body = date

# Crear un diccionario para almacenar las asignaciones de texto a keyframe
text_keyframes = {}

# Crear keyframes para mostrar las fechas correspondientes
for i, date in enumerate(unique_dates):
    frame = i + 1
    text_keyframes[frame] = str(date)

# Registrar la función de actualización para cada cambio de frame
bpy.app.handlers.frame_change_pre.append(update_date_text)

# Establecer el primer frame como inicio de la animación
bpy.context.scene.frame_set(1)


# Crea un objeto de texto
bpy.ops.object.text_add(location=(-3, 0, 0))
text_object = bpy.context.object
text_object.data.body = "Horas escuchadas"
text_object.data.extrude = 0.1
text_object.data.bevel_depth = 0.02
text_object.data.size = 4

# Configura el material del texto
material = bpy.data.materials.new(name="BlueMaterial")
material.diffuse_color = (0, 0, 1, 1)  # Color azul (RGBA)
text_object.data.materials.append(material)

# Rota el texto para que esté horizontal y paralelo al eje x
text_object.rotation_euler = (1.5708, -1.5708, 0)

# Crea un objeto de texto
bpy.ops.object.text_add(location=(-8, 0, 36))
text_object = bpy.context.object
text_object.data.body = "Top 10 Artistas"
text_object.data.extrude = 0.1
text_object.data.bevel_depth = 0.02
text_object.data.size = 4
# Configura el material del texto
material = bpy.data.materials.new(name="BlueMaterial")
material.diffuse_color = (0, 0, 1, 1)  # Color azul (RGBA)
text_object.data.materials.append(material)

# Rota el texto para que esté horizontal y paralelo al eje x
text_object.rotation_euler = (1.5708, 0, 0)
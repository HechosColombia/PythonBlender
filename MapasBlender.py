import bpy
import pandas as pd
import random

# Step 1: Prepare the scene (without deleting objects) / Paso 1: Preparar la escena (sin eliminar objetos)
def preparar_escena():
    bpy.ops.outliner.orphans_purge(do_recursive=True)

# Step 2: Load data from CSV / Paso 2: Cargar datos desde CSV
def cargar_datos(archivo):
    df = pd.read_csv(archivo, encoding='latin1', delimiter=';')
    print(df.columns)  # Show columns for debugging / Mostrar las columnas para depuración

    # Convert the year columns to numeric and divide by 1000 / Convertir las columnas de los años a numérico y dividir por 1000
    columnas_anos = df.columns[3:16]  # Assuming the year columns are in this range / Asumiendo que las columnas de los años están en este rango
    for col in columnas_anos:
        df[col] = pd.to_numeric(df[col], errors='coerce') / 1000

    return df

# Step 3: Create 3D bars and assign colors / Paso 3: Crear barras 3D y asignar colores
def crear_barras(df):
    for index, row in df.iterrows():
        nombre_objeto = str(row['numero'])
        nombre_comuna = str(row['nombre comuna'])
        comuna_obj = bpy.data.objects.get(nombre_objeto)
        
        if comuna_obj is None:
            print(f"Objeto {nombre_objeto} no encontrado en Blender.")
            continue
        
        # Create material and assign random color if it doesn't have one / Crear material y asignar color aleatorio si no tiene uno
        if not comuna_obj.data.materials:
            mat = bpy.data.materials.new(name=f"Material_{nombre_objeto}")
            mat.diffuse_color = (random.random(), random.random(), random.random(), 1)
            comuna_obj.data.materials.append(mat)
        
        # Initially set the height to the 2018 population / Inicialmente ajustar la altura a la población de 2018
        comuna_obj.scale.z = row['2018']
        comuna_obj.keyframe_insert(data_path="scale", index=2, frame=1)
        
        # Create keyframes for each year from 2018 to 2030 / Crear keyframes para cada año desde 2018 hasta 2030
        for year in range(2018, 2031):
            frame_number = (year - 2018) * 10
            comuna_obj.scale.z = row[str(year)]
            comuna_obj.keyframe_insert(data_path="scale", index=2, frame=frame_number)
        
        # Create text label at the top of the bar / Crear etiqueta de texto en la parte superior de la barra
        crear_etiqueta_texto(nombre_comuna, comuna_obj, row)

def crear_etiqueta_texto(texto, objeto, row):
    # Check if a label already exists to avoid duplicates / Verificar si ya existe una etiqueta para evitar duplicados
    if bpy.data.objects.get(f"Etiqueta_{texto}"):
        return
    
    # Create new text object / Crear nuevo objeto de texto
    bpy.ops.object.text_add(location=(0, 0, 0))
    text_obj = bpy.context.object
    text_obj.name = f"Etiqueta_{texto}"
    text_obj.scale = (800, 800, 800)
    
    # Create black material for the text / Crear material negro para el texto
    mat_texto = bpy.data.materials.new(name=f"Material_Texto_{texto}")
    mat_texto.diffuse_color = (0, 0, 0, 1)
    
    # Assign the black material to the text / Asignar el material negro al texto
    if text_obj.data.materials:
        text_obj.data.materials[0] = mat_texto
    else:
        text_obj.data.materials.append(mat_texto)
    
    # Make the text follow the object in the animation / Hacer que el texto siga el objeto en la animación
    text_obj.parent = objeto
    
    # Create custom property for the text / Crear propiedad personalizada para el texto
    text_obj["nombre_comuna"] = texto
    text_obj["valores"] = [row[str(year)] for year in range(2018, 2031)]
    text_obj["anos"] = list(range(2018, 2031))
    
    # Set the initial position of the text to a fixed height of 100 units on the Z axis / Ajustar la posición inicial del texto a una altura fija de 100 unidades en el eje Z
    text_obj.location = (objeto.location.x, objeto.location.y, 100)
    text_obj.keyframe_insert(data_path="location", frame=1)
    
    # Insert keyframes for the position of the text and custom properties / Insertar keyframes para la posición del texto y las propiedades personalizadas
    for year in range(2018, 2031):
        frame_number = (year - 2018) * 10
        text_obj.keyframe_insert(data_path="location", frame=frame_number)
        text_obj.keyframe_insert(data_path='["valores"]', frame=frame_number)
        text_obj.keyframe_insert(data_path='["anos"]', frame=frame_number)
    
    # Create dotted line to connect the text to the bar / Crear línea punteada para conectar el texto con la barra
    crear_linea(objeto, text_obj)

def crear_linea(objeto, texto_obj):
    # Create a new curve / Crear una nueva curva
    bpy.ops.curve.primitive_bezier_curve_add()
    curva_obj = bpy.context.object
    curva_obj.name = f"Linea_{texto_obj.name}"
    
    # Adjust the curve to connect the object and the text / Ajustar la curva para que conecte el objeto y el texto
    bezier_points = curva_obj.data.splines[0].bezier_points
    bezier_points[0].co = objeto.location / 6
    bezier_points[1].co = texto_obj.location
    
    # Create a new black material for the line / Crear un nuevo material negro para la línea
    mat_curva = bpy.data.materials.new(name=f"Material_Linea_{texto_obj.name}")
    mat_curva.diffuse_color = (0, 0, 0, 1.0)  # Black color with full alpha / Color negro con alfa completo
    
    # Assign the material to the curve / Asignar el material a la curva
    if len(curva_obj.data.materials) > 0:
        curva_obj.data.materials[0] = mat_curva
    else:
        curva_obj.data.materials.append(mat_curva)
    
    # Adjust the curve settings to be continuous / Ajustar la configuración de la curva para ser continua
    curva_obj.data.splines[0].use_cyclic_u = False
    curva_obj.data.splines[0].use_endpoint_u = True
    
    # Adjust the line thickness (bevel_depth) / Ajustar el grosor de la línea (bevel_depth)
    curva_obj.data.bevel_depth = 3  # Adjust this value according to the desired thickness / Ajusta este valor según el grosor deseado
    
    # Create custom property for the curve / Crear propiedad personalizada para la curva
    curva_obj.parent = objeto
    curva_obj["texto_obj"] = texto_obj.name

# Script to update text and lines on each frame / Script para actualizar el texto y las líneas en cada frame
def actualizar_texto(scene):
    frame = scene.frame_current
    for obj in bpy.data.objects:
        if "nombre_comuna" in obj.keys():
            # Calculate the index of the current and next year / Calcular el índice del año actual y el siguiente
            year_index = (frame // 10) % len(obj["anos"])
            next_year_index = (year_index + 1) % len(obj["anos"])
            
            # Calculate the interpolation values / Calcular los valores de interpolación
            start_value = obj["valores"][year_index]
            end_value = obj["valores"][next_year_index]
            interpolation_factor = (frame % 10) / 10.0
            interpolated_value = start_value + interpolation_factor * (end_value - start_value)
            
            # Calculate the current interpolated year / Calcular el año actual interpolado
            current_year = obj["anos"][year_index]
            next_year = obj["anos"][next_year_index]
            interpolated_year = current_year + interpolation_factor * (next_year - current_year)
            
            # Update the text with the interpolated values / Actualizar el texto con los valores interpolados
            obj.data.body = f"{obj['nombre_comuna']}\n{int(interpolated_year)}\n{interpolated_value:.1f}k"
        
        if obj.type == 'CURVE' and "texto_obj" in obj.keys():
            texto_obj = bpy.data.objects.get(obj["texto_obj"])
            if texto_obj:
                obj.data.splines[0].bezier_points[0].co = obj.parent.location / 6
                obj.data.splines[0].bezier_points[1].co = texto_obj.location

# Add the handler to update the text and lines on each frame change / Añadir el handler para actualizar el texto y las líneas en cada cambio de frame
bpy.app.handlers.frame_change_post.clear()
bpy.app.handlers.frame_change_post.append(actualizar_texto)

# Execute the functions / Ejecutar las funciones
preparar_escena()
archivo_csv = r'C:\Users\usuario\RutaArchivo.csv'
df = cargar_datos(archivo_csv)
crear_barras(df)

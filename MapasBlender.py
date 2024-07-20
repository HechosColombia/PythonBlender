import bpy
import pandas as pd
import random

# Paso 1: Preparar la escena (sin eliminar objetos)
def preparar_escena():
    bpy.ops.outliner.orphans_purge(do_recursive=True)

# Paso 2: Cargar datos desde CSV
def cargar_datos(archivo):
    df = pd.read_csv(archivo, encoding='latin1', delimiter=';')
    print(df.columns)  # Mostrar las columnas para depuración

    # Convertir las columnas de los años a numérico y dividir por 1000
    columnas_anos = df.columns[3:16]  # Asumiendo que las columnas de los años están en este rango
    for col in columnas_anos:
        df[col] = pd.to_numeric(df[col], errors='coerce') / 1000

    return df

# Paso 3: Crear barras 3D y asignar colores
def crear_barras(df):
    for index, row in df.iterrows():
        nombre_objeto = str(row['numero'])
        nombre_comuna = str(row['nombre comuna'])
        comuna_obj = bpy.data.objects.get(nombre_objeto)
        
        if comuna_obj is None:
            print(f"Objeto {nombre_objeto} no encontrado en Blender.")
            continue
        
        # Crear material y asignar color aleatorio si no tiene uno
        if not comuna_obj.data.materials:
            mat = bpy.data.materials.new(name=f"Material_{nombre_objeto}")
            mat.diffuse_color = (random.random(), random.random(), random.random(), 1)
            comuna_obj.data.materials.append(mat)
        
        # Inicialmente ajustar la altura a la población de 2018
        comuna_obj.scale.z = row['2018']
        comuna_obj.keyframe_insert(data_path="scale", index=2, frame=1)
        
        # Crear keyframes para cada año desde 2018 hasta 2030
        for year in range(2018, 2031):
            frame_number = (year - 2018) * 10
            comuna_obj.scale.z = row[str(year)]
            comuna_obj.keyframe_insert(data_path="scale", index=2, frame=frame_number)
        
        # Crear etiqueta de texto en la parte superior de la barra
        crear_etiqueta_texto(nombre_comuna, comuna_obj, row)

def crear_etiqueta_texto(texto, objeto, row):
    # Verificar si ya existe una etiqueta para evitar duplicados
    if bpy.data.objects.get(f"Etiqueta_{texto}"):
        return
    
    # Crear nuevo objeto de texto
    bpy.ops.object.text_add(location=(0, 0, 0))
    text_obj = bpy.context.object
    text_obj.name = f"Etiqueta_{texto}"
    text_obj.scale = (800, 800, 800)
    
    # Crear material negro para el texto
    mat_texto = bpy.data.materials.new(name=f"Material_Texto_{texto}")
    mat_texto.diffuse_color = (0, 0, 0, 1)
    
    # Asignar el material negro al texto
    if text_obj.data.materials:
        text_obj.data.materials[0] = mat_texto
    else:
        text_obj.data.materials.append(mat_texto)
    
    # Hacer que el texto siga el objeto en la animación
    text_obj.parent = objeto
    
    # Crear propiedad personalizada para el texto
    text_obj["nombre_comuna"] = texto
    text_obj["valores"] = [row[str(year)] for year in range(2018, 2031)]
    text_obj["anos"] = list(range(2018, 2031))
    
    # Ajustar la posición inicial del texto a una altura fija de 100 unidades en el eje Z
    text_obj.location = (objeto.location.x, objeto.location.y, 100)
    text_obj.keyframe_insert(data_path="location", frame=1)
    
    # Insertar keyframes para la posición del texto y las propiedades personalizadas
    for year in range(2018, 2031):
        frame_number = (year - 2018) * 10
        text_obj.keyframe_insert(data_path="location", frame=frame_number)
        text_obj.keyframe_insert(data_path='["valores"]', frame=frame_number)
        text_obj.keyframe_insert(data_path='["anos"]', frame=frame_number)
    
    # Crear línea punteada para conectar el texto con la barra
    crear_linea(objeto, text_obj)

def crear_linea(objeto, texto_obj):
    # Crear una nueva curva
    bpy.ops.curve.primitive_bezier_curve_add()
    curva_obj = bpy.context.object
    curva_obj.name = f"Linea_{texto_obj.name}"
    
    # Ajustar la curva para que conecte el objeto y el texto
    bezier_points = curva_obj.data.splines[0].bezier_points
    bezier_points[0].co = objeto.location / 6
    bezier_points[1].co = texto_obj.location
    
    # Crear un nuevo material negro para la línea
    mat_curva = bpy.data.materials.new(name=f"Material_Linea_{texto_obj.name}")
    mat_curva.diffuse_color = (0, 0, 0, 1.0)  # Color negro con alfa completo
    
    # Asignar el material a la curva
    if len(curva_obj.data.materials) > 0:
        curva_obj.data.materials[0] = mat_curva
    else:
        curva_obj.data.materials.append(mat_curva)
    
    # Ajustar la configuración de la curva para ser continua
    curva_obj.data.splines[0].use_cyclic_u = False
    curva_obj.data.splines[0].use_endpoint_u = True
    
    # Ajustar el grosor de la línea (bevel_depth)
    curva_obj.data.bevel_depth = 3  # Ajusta este valor según el grosor deseado
    
    # Crear propiedad personalizada para la curva
    curva_obj.parent = objeto
    curva_obj["texto_obj"] = texto_obj.name

# Script para actualizar el texto y las líneas en cada frame
def actualizar_texto(scene):
    frame = scene.frame_current
    for obj in bpy.data.objects:
        if "nombre_comuna" in obj.keys():
            # Calcular el índice del año actual y el siguiente
            year_index = (frame // 10) % len(obj["anos"])
            next_year_index = (year_index + 1) % len(obj["anos"])
            
            # Calcular los valores de interpolación
            start_value = obj["valores"][year_index]
            end_value = obj["valores"][next_year_index]
            interpolation_factor = (frame % 10) / 10.0
            interpolated_value = start_value + interpolation_factor * (end_value - start_value)
            
            # Calcular el año actual interpolado
            current_year = obj["anos"][year_index]
            next_year = obj["anos"][next_year_index]
            interpolated_year = current_year + interpolation_factor * (next_year - current_year)
            
            # Actualizar el texto con los valores interpolados
            obj.data.body = f"{obj['nombre_comuna']}\n{int(interpolated_year)}\n{interpolated_value:.1f}k"
        
        if obj.type == 'CURVE' and "texto_obj" in obj.keys():
            texto_obj = bpy.data.objects.get(obj["texto_obj"])
            if texto_obj:
                obj.data.splines[0].bezier_points[0].co = obj.parent.location / 6
                obj.data.splines[0].bezier_points[1].co = texto_obj.location

# Añadir el handler para actualizar el texto y las líneas en cada cambio de frame
bpy.app.handlers.frame_change_post.clear()
bpy.app.handlers.frame_change_post.append(actualizar_texto)

# Ejecutar las funciones
preparar_escena()
archivo_csv = r'C:\Users\usuario\RutaArchivo.csv'
df = cargar_datos(archivo_csv)
crear_barras(df)
import csv
#para manejar SQLServer
import pyodbc 

#try esta puesto para el manejo de errores
try:
    #Conexión a la base de datos SQL Server
    conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=servidor;DATABASE=SegurAr;UID=usuario;PWD=contraseña')
    cursor = conexion.cursor()

    #Crear la tabla en SQLServer
    cursor.execute('''
    CREATE TABLE clientes (
            Nombre VARCHAR(255),
            Edad INT,
            Ciudad VARCHAR(255)
            DNI VARCHAR(30)
            AnoDeNacimiento INT
            )
    ''')

    #Abrir el archivo CSV y leer su contenido
    with open('clientes.csv', 'r') as archivo_csv:
        lectura_csv = csv.reader(archivo_csv)
        next(lectura_csv)  #Saltar la primera linea
        for fila in lectura_csv:
            try:
                #Validar y convertir los datos, para que no haya errores
                nombre = fila[0]
                edad = int(fila[1])   #Convertir a entero
                ciudad = fila[2]
                dni = str(fila[3])    #Convertir a string
                año_de_nacimiento = int(fila[4])    #Convertir a entero
                año_de_nacimiento = 1900 + año_de_nacimiento 

                #Insertar cada fila en la tabla
                cursor.execute(
                    'INSERT INTO clientes (Nombre, Edad, Ciudad, DNI, AnoDeNacimiento) VALUES (?, ?, ?, ?, ?)', 
                    (nombre, edad, ciudad, dni, año_de_nacimiento))
                
            except ValueError as ve:
                print(f"Error al convertir datos: {ve}. Fila: {fila}")
            except pyodbc.Error as db_err:
                print(f"Error al insertar en la base de datos: {db_err}. Fila: {fila}")

    #Confirmar y cerrar
    conexion.commit()
except pyodbc.Error as e:
    print(f"Error de conexión o ejecución: {e}")
finally:
    if conexion:
        conexion.close()

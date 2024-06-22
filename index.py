from zfunctions.f import *


# CREAR ARCHIVO DE TEXTO SIMPLE
crear_archivo_texto('hola 2.txt', '1QILVCSGy94N4k5C--tOIzJojmltVa6E0', 'hola')


# DESGARGAR ARCHIVOS DE GOOGLE_DISK/CARPETA
leer_y_descargar_archivos('1QILVCSGy94N4k5C--tOIzJojmltVa6E0', 'download')


# LEER CARPETA DOWNLOAD Y ENVIAR POR CORREO
send_email_with_attachments('suzdalenko.suzdalenko@gmail.com', 'email', 'password')

# ELIMINAR ARCHIVOS MAYORES A 1 MES
delete_old_files()
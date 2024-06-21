from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# Autenticación y creación del cliente de PyDrive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  

drive = GoogleDrive(gauth)
   
# ID del archivo de Google Drive
#   file_id = 'TU_FILE_ID_AQUI'
#   
# Descargar el archivo
#   file = drive.CreateFile({'id': file_id})
#   file.GetContentFile('archivo_descargado.extension')
#   
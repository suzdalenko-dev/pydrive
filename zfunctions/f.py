import os, smtplib, shutil
from datetime import datetime, timedelta
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from email.message import EmailMessage

# inicio login
def login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile('credentials_module.json')
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile('credentials_module.json')
    return GoogleDrive(gauth)
   
# CREAR ARCHIVO DE TEXTO SIMPLE
def crear_archivo_texto(file_name, folder_id, content):
    credentials = login()
    mFile = credentials.CreateFile({ 'title': file_name, 'parents': [{'id': folder_id}]})
    mFile.SetContentString(content)
    mFile.Upload()





# DESGARGAR ARCHIVOS DE UNA CARPETA
def leer_y_descargar_archivos(folder_id, download_folder):
    credentials = login()
    file_list = credentials.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    for file in file_list:
        file_id = file['id']
        file_name = file['title']
        file.GetContentFile(os.path.join(download_folder, file_name))
        print(f'Downloaded: {file_id} {file_name}')
        # Move the file to trash
        file.Trash()
        print(f'Moved to trash: {file_id} {file_name}')







# LEER CARPETA DOWNLOAD Y ENVIAR POR CORREO Y MOVER ARCHIVO
def send_email_with_attachments(to_email, from_email, password):
    attachments = [os.path.join('download', file_name) for file_name in os.listdir('download')]

    msg = EmailMessage()
    msg['Subject'] = 'Imagenes Google Disk'
    msg['From'] = from_email
    msg['To'] = 'loj.rus@gmail.com'
    msg.set_content(datetime.now().strftime('%H:%M:%S %m/%d/%Y'))
    
    for attachment_path in attachments:
        file_name = os.path.basename(attachment_path)
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_type = 'application/octet-stream'
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(from_email, password)
            smtp.send_message(msg)
    except Exception as e:
        pass

    msg = EmailMessage()
    msg['Subject'] = 'Imagenes Google Disk'
    msg['From'] = from_email
    msg['To'] = to_email
    msg.set_content(datetime.now().strftime('%H:%M:%S %m/%d/%Y'))
    
    for attachment_path in attachments:
        file_name = os.path.basename(attachment_path)
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_type = 'application/octet-stream'
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(from_email, password)
            smtp.send_message(msg)
        print(f'Email sent successfully to {to_email} with attachments: {attachments}')
        x = True
    except Exception as e:
        print(f'Failed to send email to {to_email}. Error: {str(e)}')
        x =  False

    if x == True:
        for file_name in os.listdir('download'):
            src_path = os.path.join('download', file_name)
            dest_path = os.path.join('sent', file_name)
            shutil.move(src_path, dest_path)
            print(f'Moved {file_name}')   






# Function to delete files older than 1 month in the 'sent' folder
def delete_old_files():
    now = datetime.now()
    one_month_ago = now - timedelta(days=11)

    for file_name in os.listdir('sent'):
        file_path = os.path.join('sent', file_name)
        if os.path.isfile(file_path):
            file_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_modified_time < one_month_ago:
                os.remove(file_path)
                print(f'Deleted old file: {file_name}')
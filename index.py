import requests
from zfunctions.f import *

# ir a buscar url de imagenes a servidor froxa
headers = {'User-Agent': 'Google'}
response = requests.get('https://intranet.froxa.net/aimagen/give_me_pictures_of_yesterday_and_today.php', headers=headers)

if response.status_code == 200:
    data = response.json()
    if data['res'] == 'ok':
        x = data['last_day']
        y = data['today']
        # guardo la primera imagen localmente
        respuesta = requests.get(x)
        if respuesta.status_code == 200:
            nombre_archivo = 'download/'+os.path.basename(x)
            
            with open(nombre_archivo, 'wb') as archivo:
                archivo.write(respuesta.content)
        else:
            print(f"Error x: {respuesta.status_code}")
        # guardo la segunda imagen localmente
        respuesta = requests.get(y)
        if respuesta.status_code == 200:
            nombre_archivo = 'download/'+os.path.basename(y)
            
            with open(nombre_archivo, 'wb') as archivo:
                archivo.write(respuesta.content)
        else:
            print(f"Error y: {respuesta.status_code}")
        # envio correo con enlaces y archivos
        send_email_with_attachments('alexey.suzdalenko@froxa.com', 'froxa.app@gmail.com', 'xlganerhawjkiiar', x, y)
else:
    print(f'Error: {response.status_code}')


# elimino arhivos locales de mas de 11 dias
delete_old_files()
# elimino archivos en servidor froxa 
res = requests.get('https://intranet.froxa.net/aimagen/delete_forder.php', headers=headers)
data = res.json()
print(data)
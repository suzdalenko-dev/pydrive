import requests
from zfunctions.f import *

headers = {'User-Agent': 'Google'}
response = requests.get('https://intranet.froxa.net/aimagen/give_me_pictures_of_yesterday_and_today.php', headers=headers)

if response.status_code == 200:
    data = response.json()

    if data['res'] == 'ok':
        x = data['last_day']
        y = data['today']
        send_email_with_attachments('alexey.suzdalenko@froxa.com', 'froxa.app@gmail.com', 'xlganerhawjkiiar', x, y)
        print(data)
else:

    print(f'Error: {response.status_code}')

print(response)
import requests
import json

email = ""
password = ""
teslaUrl = 'https://owner-api.teslamotors.com/oauth/token'
teslaAPI = 'https://owner-api.teslamotors.com/api/1/'
vehicleID = ''
carChoice = -1
encodedURL = teslaAPI+'vehicles/'+vehicleID
choice = 'help'

data = {
        'grant_type' : 'password',
        'client_id' : '81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384',
        'client_secret' : 'c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3',
        'email' : email,
        'password' password
        }

r = requests.post(teslaUrl, data = data)
token = r.json()['access_token']

print(token)

headers = {
          'Authorization' : 'Bearer '+token
        }

print('\n')

r = requests.get(teslaAPI+'vehicles/', headers = headers)
for ind, val in enumerate(r.json()['response']):
    print(str(ind)+" "+val['display_name'])

print('\n')

while ((int(carChoice) < 0) or (int(carChoice) > len(r.json()['response'])-1)):
    carChoice = input('Which car do you want to control?: ')

print('\n')

vehicleID = r.json()['response'][int(carChoice)]['id']
encodedURL = teslaAPI+'vehicles/'+str(vehicleID)

apiChoices = {
        'help'      : ('help', 0, 'shows this menu'),
        'list'      : (teslaAPI+'vehicles/', 1, 'lists all cars'),
        'mobile'    : (encodedURL+'/mobile_enabled', 1, 'display if car can be connected to'),
        'charge'    : (encodedURL+'/data_request/charge_state', 1, 'charge state details'),
        'climate'   : (encodedURL+'/data_request/climate_state', 1, 'in-car climate details'),
        'drive'     : (encodedURL+'/data_request/drive_state', 1, 'drive state (speed, gear, etc.)'),
        'gui'       : (encodedURL+'/data_request/gui_settings', 1, 'gui options enabled in vehicle'),
        'vehicle'   : (encodedURL+'/data_request/vehicle_state', 1, 'vehicle details (location)'),
        'wakeup'    : (encodedURL+'/wake_up', 0, 'wake up vehicle to enable more information'),
        'chargeopen': (encodedURL+'/command/charge_port_door_open', 0, 'open charge opert'),
        'stopcharge': (encodedURL+'/command/charge_stop', 0, 'stop charging'),
        'flash'     : (encodedURL+'/command/flash_lights', 0, 'flash lights'),
        'honk'      : (encodedURL+'/command/honk_horn', 0, 'honk horn'),
        'unlock'    : (encodedURL+'/command/door_unlock', 0, 'unlock car'),
        'lock'      : (encodedURL+'/command/door_lock', 0, 'lock car'),
        'quit'      : ('quit',  0,  'quits')
        }


while (choice != 'quit'):
    if (choice == 'help') :
        for key, value in apiChoices.items() :
            print(key+" : "+value[2])
    elif (choice in apiChoices):
        apiChoice = apiChoices.get(choice)
        if (apiChoice[1]):
            r = requests.get(apiChoice[0], headers = headers)
        else:
            r = requests.post(apiChoice[0], headers = headers)
        print(json.dumps(r.json(), indent = 2))
    else:
        print('Not a valid choice. (help)')
    print('\n')
    choice = input('What do you want to see (help): ')
    print('\n')

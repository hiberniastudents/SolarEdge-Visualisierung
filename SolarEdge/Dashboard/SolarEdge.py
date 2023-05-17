from solaredge.api.client import Client
import datetime
import json


today = datetime.datetime.now()

today_date = today.strftime("%Y-%m-%d")
today_date_time = today.strftime("%Y-%m-%d %H:%M:%S")
today_date_time_beginn = today_date + ' 00:00:00'
today_time = today.strftime("%H:%M")
today_hour_in_sec = datetime.timedelta(hours=today.hour, minutes=today.minute).seconds
today_hour = float(float(today_hour_in_sec) / 3600)
today_quarter_num = int(today_hour / 0.25)


API_KEY = 'FRUFGTE3ISBRDDTKIBOIB02BX0A2PG03'
SITE_ID_1 = '3631874' # Gebäude P
SITE_ID_2 = '3637342' # Gebäude M


se_client = Client()
se_client.set_api_key(API_KEY)
site = se_client.sites.get_sites()


# Anlage 1
def unit1():
    installation_date_1 = site['sites']['site'][1]['installationDate']
    installation_date_time_1 = installation_date_1 + ' 00:00:00'

    power_1 = se_client.sites.get_power(SITE_ID_1, today_date_time_beginn, today_date_time)
    current_power_1 = power_1['power']['values'][today_quarter_num]['value']
    if current_power_1 == None:
        current_power_1 = 0
    


    energy_1 = se_client.sites.get_energy(SITE_ID_1, today_date, today_date, 'DAY')
    current_energy_1 = energy_1['energy']['values'][0]['value']

    unit1_powers = dict()

    for x in range(today_quarter_num + 1):
        if x == 0:
            continue
        power = power_1['power']['values'][x]['value']
        if power == None:
            power = 0
        unit1_powers[x] = power


    unit1_dict = dict(unit = 1, installation_date = installation_date_1, current_date = today_date, current_power = current_power_1, current_energy = current_energy_1, power_of_day = unit1_powers)

    return unit1_dict


# Anlage 2
def unit2():
    installation_date_2 = site['sites']['site'][0]['installationDate']
    installation_date_time_2 = installation_date_2 + ' 00:00:00'


    power_2 = se_client.sites.get_power(SITE_ID_2, today_date_time_beginn, today_date_time)
    current_power_2 = power_2['power']['values'][today_quarter_num]['value']
    if current_power_2 == None:
        current_power_2 = 0


    energy_2 = se_client.sites.get_energy(SITE_ID_2, today_date, today_date, 'DAY')
    current_energy_2 = energy_2['energy']['values'][0]['value']

    unit2_powers = dict()

    for x in range(today_quarter_num + 1):
        if x == 0:
            continue
        power = power_2['power']['values'][x]['value']
        if power == None:
            power = 0
        unit2_powers[x] = power
    
    unit2_dict = dict(unit = 2, installation_date = installation_date_2, current_date = today_date, current_power = current_power_2, current_energy = current_energy_2, power_of_day = unit2_powers)

    return unit2_dict

#unit1_data = unit1()
#unit2_data = unit2()

def all(unit1_data, unit2_data):
    power_all = int(unit1_data['current_power']) + int(unit2_data['current_power'])
    energy_all = int(unit1_data['current_energy']) + int(unit2_data['current_energy'])
    all_dict = dict(power = power_all, energy = energy_all)
    return all_dict

'''
print('Anlage 1')
print('Installation Date: ' + unit1_data['installation_date'])
print('Energy: ' + str(unit1_data['current_energy']) + ' Wh')
print('Power: ' + str(unit1_data['current_power']) + ' W')
print('\n')
print('Anlage 2')
print('Installation Date: ' + unit2_data['installation_date'])
print('Energy: ' + str(unit2_data['current_energy']) + ' Wh')
print('Power: ' + str(unit2_data['current_power']) + ' W')
print('\n')
print('Gesamt')
print('Energy: ' + str((energy_all / 1000)) + ' kWh')
print('Power: ' + str(power_all) + ' W')
print('\n')
'''


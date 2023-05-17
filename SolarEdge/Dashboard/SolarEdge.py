from solaredge.api.client import Client
import datetime


today = datetime.datetime.now()

today_date = today.strftime("%Y-%m-%d")
today_date_1 = datetime.datetime.now().date()
today_date_time = today.strftime("%Y-%m-%d %H:%M:%S")
today_date_time_beginn = today_date + ' 00:00:00'
today_time = today.strftime("%H:%M")
today_hour_in_sec = datetime.timedelta(hours=today.hour, minutes=today.minute).seconds
today_hour = float(float(today_hour_in_sec) / 3600)
today_quarter_num = int(today_hour / 0.25)
date_7_days = today_date_1 - datetime.timedelta(days=7)



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
        power_day_until_now = 0
        power_day_until_now = float(power_day_until_now) + float(power)
        energy_day_until_now = float(power_day_until_now) * 0.25

    unit1_dict = dict(unit = 1, installation_date = installation_date_1, current_date = today_date, current_power = current_power_1, current_energy = current_energy_1, power_day_until_now = power_day_until_now, energy_day_until_now = energy_day_until_now, power_of_day = unit1_powers)
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
        power_day_until_now = 0
        power_day_until_now = float(power_day_until_now) + float(power)
        energy_day_until_now = float(power_day_until_now) * 0.25
    
    unit2_dict = dict(unit = 2, installation_date = installation_date_2, current_date = today_date, current_power = current_power_2, current_energy = current_energy_2, power_day_until_now = power_day_until_now, energy_day_until_now = energy_day_until_now, power_of_day = unit2_powers)

    return unit2_dict

'''
def energy_7_days():
    energy_1 = se_client.sites.get_energy(SITE_ID_1, date_7_days, today_date, 'DAY')
    energy_2 = se_client.sites.get_energy(SITE_ID_2, date_7_days, today_date, 'DAY')
    watt_day_hour = dict()
    for i in range(665):
        print(i)
        if i == 0:
            continue
        power1 = energy_1['energy']['values'][i]['value']
        power2 = energy_2['energy']['values'][i]['value']
        power = int(power1) + int(power2)
        watt_day_hour[i] = power
        i = i +4

    energy_7_days = int(energy_1['energy']['values'][0]['value']) + int(energy_2['energy']['values'][0]['value'])
    energy_7_days_dict = dict(energy_7_days = energy_7_days, watt_day_hour = watt_day_hour)
    return energy_7_days_dict

print(energy_7_days())
'''
#unit1_data = unit1()
#unit2_data = unit2()

def all(unit1_data, unit2_data):
    print(unit1_data['energy_day_until_now'])
    print(unit2_data['energy_day_until_now'])
    energy_day_until_now = float(unit1_data['energy_day_until_now']) + float(unit2_data['energy_day_until_now'])
    print(energy_day_until_now)
    power_all = float(unit1_data['current_power']) + float(unit2_data['current_power'])
    print(unit1_data['current_power'])
    print(unit2_data['current_power'])
    energy_all = float(unit1_data['current_energy']) + float(unit2_data['current_energy'])
    all_dict = dict(power = power_all, energy = energy_all, energy_day_until_now = energy_day_until_now)
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


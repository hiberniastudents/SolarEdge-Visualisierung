# Dieses Skript kann variable für jede Anlage daten abrufen die in der SolarConfig.py definiert sind.
import requests # Zum erfassen der API Daten
import SolarConfig # Für die Einfachheit der Anlagen ID und des API Keys
import json
from datetime import datetime, timedelta 
from collections import OrderedDict 

api_key = SolarConfig.API_KEY 
site_ids = SolarConfig.SITE_IDs



# Das Erhalten der Daten und die Umformung in Python von JSON
def solardata(site_id):
        solaredge = 'https://monitoringapi.solaredge.com/%20site/'+ site_id + '/overview.json?api_key=' +api_key # Das Erhalten der Daten von Solaredge
        json_data = requests.get(solaredge).json() # Definierung für die JSON Request
        lastupdatetime = json_data['overview']['lastUpdateTime']
        totalenergy = json_data['overview']['lifeTimeData']['energy']/1000
        lastyearenergy = json_data['overview']['lastYearData']['energy']/1000
        lastmonthenergy = json_data['overview']['lastMonthData']['energy']/1000
        lastdayenergy = json_data['overview']['lastDayData']['energy']/1000
        currentpower = json_data['overview']['currentPower']['power']
        return {'lastupdatetime':lastupdatetime,'totalenergy': totalenergy,'lastyearenergy': lastyearenergy,'lastmonthenergy': lastmonthenergy,'lastdayenergy': lastdayenergy,'currentpower': currentpower}

# Defenierung der Variablen für alle Anlagen     
total_energyofalltime = 0
total_lastyearenergy = 0
total_lastmonthenergy = 0
total_lastdayenergy = 0
total_currentpower = 0

for Site_ID in site_ids:
    Data = solardata(Site_ID)
    globals()[f"totalenergy_{Site_ID}"] = Data['totalenergy']
    globals()[f"lastyearenergy_{Site_ID}"] = Data['lastyearenergy']
    globals()[f"lastmontenergy_{Site_ID}"] = Data['lastmonthenergy']
    globals()[f"lastdayenergy_{Site_ID}"] = Data['lastdayenergy']
    globals()[f"currentpower_{Site_ID}"] = Data['currentpower']
    total_energyofalltime += globals()[f"totalenergy_{Site_ID}"]
    total_lastyearenergy += globals()[f"lastyearenergy_{Site_ID}"]
    total_lastmonthenergy += globals()[f"lastmontenergy_{Site_ID}"]
    total_lastdayenergy += globals()[f"lastdayenergy_{Site_ID}"]
    total_currentpower += globals()[f"currentpower_{Site_ID}"] 

     

# Teilen der Werte in lesbare bereiche
total_lastyearenergy = (total_lastyearenergy)/1000     # Energie des Jahres in MWh=> geteilt durch 1000
total_lastmonthenergy = (total_lastmonthenergy)/1000    # Energie des Monats in MWh=> geteilt durch 1000
total_currentpower = (total_currentpower)/1000           # Energie die Gerade produziert wird in kW=> geteilt durch 1000

# Um gerundete 2 Nachkommastellen zu bekommen
t_eoat = round((total_energyofalltime)/1000, 3)    # Energie über das gesamte "Leben" der Anlage=> eoat - energy of all time, in MWh=> durch 1000
t_lye = round(total_lastyearenergy, 3)      # Energie des Jahres=> lye - last year energy
t_lme = round(total_lastmonthenergy, 3)     # Energie des Monats=> lme - last month energy
t_lde = round(total_lastdayenergy, 2)       # Energie des Tages=> lde - last day energy
t_cp = round(total_currentpower, 2)         # Energie die Gerade produziert wird=> cp - current power

#Berechnung des CO2 Fußabdrucks
g_kwh = 392 # CO2 Faktor = 392 g/kWh laut Solar Edge (EPA)
trees_kwh = 0.0117 # Gepflanzte Bäume Faktor = 0,0117 Bäume pro geparte kWh laut Solar Edge (EPA)
home_kwh = 4500 # Durchschnittlicher Stromverbrauch eines Haushalts in kWh pro Tag laut Umweltbundesamt
saved_co2 = round((total_energyofalltime * g_kwh)/1000, 2) # Eingesparte CO2 Emissionen in kg=> durch 1000
planted_trees = round(total_energyofalltime * trees_kwh, 2) # Gepflanzte Bäume
homes = round(total_energyofalltime / home_kwh, 2) # Anzahl der Haushalte die mit der Energie versorgt werden könnten

def save_current_today():
    date = datetime.now().strftime("%d.%m.%Y")
    time = datetime.now().strftime("%H:%M")
    print(f"Save the current and Energy {date}, {time}")
    try:
        with open("data/currentpower.json", "r") as file:
            current_dict = json.load(file)
    except:
        current_dict = dict()   
    if datetime.now().strftime("%M") == "00" or datetime.now().strftime("%M") == "30":
        if date not in current_dict:
            new_date = {date:{time:t_cp}}
            current_dict.update(new_date)
        else:
            current_dict[date][time] = t_cp
        with open("data/currentpower.json", "w") as file:
            json.dump(current_dict, file, indent=4)
    time_list = []
    current_list = []
    if date not in current_dict:
        print("Please let the script until the next full hour or half hour to geht the data")
        last_7_day = ''
        last_7_energy = ''
    else:
        for time_today in current_dict[date]:
            time_dict_list = [str(time_today)]
            time_list.extend(time_dict_list)
            current_dict_list = [current_dict[date][time_today]]
            current_list.extend(current_dict_list)
        last_7_day, last_7_energy = save_day_energy(date)
    return time_list, current_list, last_7_day, last_7_energy
             
def save_day_energy(date):
    try:
        with open("data/timeanddate.json", "r") as dayfile:
            day_dict = json.load(dayfile, object_pairs_hook=OrderedDict)
    except:
        day_dict = dict()
    day_dict[date] = t_lde
    with open("data/timeanddate.json", "w") as dayfile:
        json.dump(day_dict, dayfile, indent=4)

    last_7_entries = list(day_dict.items())[-7:]
    last_7_day = [entry[0] for entry in last_7_entries]
    last_7_energy = [entry[1] for entry in last_7_entries]
    return last_7_day, last_7_energy
    

 

# Debugging Code bitte nicht auskommentieren
"""
print(f"Energy all Time {t_eoat}") #in MWh
print(f"Energy last Year {t_lye}")
print(f"Energy last Month {t_lme}")
print(f"Energy last Day {t_lde}")
print(f"Current Power {t_cp}")
print(f"Saved CO2 {saved_co2}")
print(f"Planted Trees {planted_trees}")
print(f"Homes {homes}")
"""
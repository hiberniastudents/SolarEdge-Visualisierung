import dataclasses
from flask import Flask, render_template, request
import time
from apscheduler.schedulers.background import BackgroundScheduler
#import total # Importiert die Daten von den Anlagen GM und GP
import Data as total # imortiert die Daten aus dem Data.py Skript welches Variable für anzahl x anlagen erstellt und verrechnet
#from flask import request
import SolarConfig

app = Flask(__name__)
sched = BackgroundScheduler(daemon=True)
sched.add_job(total.save_current_today,'interval',minutes=1) # Run the data save function ervery minute
sched.start()




@app.route("/")
def home():
    t_eoat = total.t_eoat
    t_lye = total.t_lye
    t_lme = total.t_lme
    t_lde = total.t_lde
    t_cp = total.t_cp
    saved_co2 = total.saved_co2
    planted_trees = total.planted_trees
    homes = total.homes
    time_list, current_list, last_7_day, last_7_energy = total.save_current_today()
    color =[SolarConfig.COLOR_TEXT, SolarConfig.COLOR_TOP_BACKGROUND, SolarConfig.COLOR_TOP_TEXT]

    embed = request.args.get('embed')
    if embed == 'true':
        return render_template('embed.html', color=color, teoat=t_eoat, tlye=t_lye, tlme=t_lme, tlde=t_lde, tcp=t_cp, savedco2=saved_co2, plantedtrees=planted_trees, homes=homes, logo_url=SolarConfig.Logo_URL, title=SolarConfig.TITLE_EMBED)
    else:
        return render_template('index.html', color=color, teoat=t_eoat, tlye=t_lye, tlme=t_lme, tlde=t_lde, tcp=t_cp, savedco2=saved_co2, plantedtrees=planted_trees, homes=homes, logo_url=SolarConfig.Logo_URL, title=SolarConfig.TITLE_MAIN, current_list=current_list, time_list=time_list, last_7_day=last_7_day, last_7_energy=last_7_energy)
        

if __name__ == '__main__':
    app.run(host="0.0.0.0")

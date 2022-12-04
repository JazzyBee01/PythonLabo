import sqlite3
import datetime
from math import floor
import matplotlib.pyplot as plt
import pandas as pd

import numpy as np
from flask import Flask, render_template
app = Flask(__name__)

class databaseOperations():
    def __init__(self, database="../9_veloDatabank/veloDatabase.db"):
        self.dbName = database

        self.legeStations = []
        self.volleStations = []

        self.set_legeStations()
        self.set_volleStations()

        self.aantalLeeg = len(self.legeStations)
        self.aantalVol = len(self.volleStations)

    def printResult(self, res):
        for line in res:
            print(line)

    def get_currTimefield(self):
        t = datetime.datetime.now()
        if t.minute >= 30:
            field = f"H{t.hour}_30"
        else:
            field = f"H{t.hour}_00"
        return field

    def execute(self, query):
        con = sqlite3.connect(self.dbName)
        cur = con.cursor()
        res = cur.execute(query)
        #self.printResult(res)
        con.commit()
        return res

    # geeft het aantal lege stations en de namen van de lege stations
    def get_stationsMetAantalVelos(self, aantalVelos):
        currTimeField = self.get_currTimefield()
        query = f"SELECT " \
                f"st.id, " \
                f"st.address " \
                f"FROM " \
                f"stations st, " \
                f"historiek h " \
                f"WHERE " \
                f"st.id = h.id " \
                f"AND h.{currTimeField} = {aantalVelos};"

        res = self.execute(query)
        stations = []
        for line in res:
            stations.append({"id": line[0], "address": line[1]})
        return stations

    def set_legeStations(self):
        self.legeStations = self.get_stationsMetAantalVelos(0)
        return self.legeStations

    def set_volleStations(self):
        currTimeField = self.get_currTimefield()
        query = f"SELECT " \
                f"st.id, " \
                f"st.address " \
                f"FROM " \
                f"stations st, " \
                f"historiek h " \
                f"WHERE " \
                f"st.id = h.id " \
                f"AND h.{currTimeField} = st.total_slots;"

        res = self.execute(query)
        stations = []
        for line in res:
            stations.append({"id": line[0], "address": line[1]})
        self.volleStations = stations
        return self.volleStations

    #time weergegeven als 21,5 -> 21:30
    def timeToField(self, time):
         if time%1 == 0.5:
             return f"H{floor(time)}_30"
         else:
             return f"H{floor(time)}_00"
    #time weergegeven als 21,5 -> 21:30

    def compareTimes(self, time):
        if time != 0:
            prev_time = time - 0.5
        else:
            prev_time = 23.5

        ref = self.timeToField(time)
        prev = self.timeToField(prev_time)

        query = f"SELECT id, {ref} - {prev} FROM historiek "
        #print(query)
        res = self.execute(query)

        weggenomen = 0
        teruggezet = 0

        for line in res:
            if line[1]:
                if line[1] < 0:
                    weggenomen -= line[1]
                if line[1] > 0:
                    teruggezet += line[1]

        #print(weggenomen, teruggezet)
        return [weggenomen, teruggezet]

    def get_verplaatsingen(self):
        verp = []
        a = np.linspace(0, 23.5, 48)
        for i in a:
            #print(i)
            verp.append(self.compareTimes(i))
        return verp

    def generatePlot(self, targetFileName):
        verp = []
        for i in self.get_verplaatsingen():
            verp.append(i[1]) #neemt enkel de weggenomen fietsen
        #print(verp)
        #print(len(verp))

        #print(np.linspace(0, 23.5, 48))
        #print(len(np.linspace(0, 23.5, 48)))

        df = pd.DataFrame({
            'x_axis': np.linspace(0, 23.5, 48),
            'y_axis': verp
        })

        # plot
        plt.plot('x_axis', 'y_axis', data=df, linestyle='-', marker='o')
        plt.savefig(targetFileName)
        return plt


data = databaseOperations("../9_veloDatabank/veloDatabase.db")
data.generatePlot("verplaatsingen.png")

@app.route("/")
def hello_world():
    return render_template('index.html', legeStations = data.legeStations, aantalLeeg = len(data.legeStations), volleStations = data.volleStations, aantalVol = len(data.volleStations))
    #return render_template('index.html', legeStations=[{"id": 1, "name": "piet"},{"id": 2, "name": "jos"}])


@app.route("/historiek")
def historiek():
    return render_template('historiek.html')

@app.route("/stations")
def stations():
    return render_template('stations.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404



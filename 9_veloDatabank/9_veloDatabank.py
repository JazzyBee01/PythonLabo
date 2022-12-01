import sqlite3
from urllib.request import urlopen
import datetime; import calendar; import time
import json


class VeloDatabaseCreator:
      def __init__(self):
            self.url = "https://www.velo-antwerpen.be/availability_map/getJsonObject"
            self.db = "veloDatabase.db"
            self.t = None
            self.epoch = None
            self.data_json = None

            self.set_t()
            self.read_json()

      def read_json(self):
            #url = "https://www.velo-antwerpen.be/availability_map/getJsonObject"
            response = urlopen(self.url)
            self.data_json = json.loads(response.read())

      def set_t(self):
            self.t = datetime.datetime.now()
            self.epoch = calendar.timegm(self.t.timetuple())

      def setupDB(self):
            self.read_json()
            self.set_t()
            con = sqlite3.connect("veloDatabase.db")
            cur = con.cursor()
            # table stations aanmaken
            cur.execute(f"CREATE TABLE if not exists stations"
                  f"(id INTEGER PRIMARY KEY,"
                  f" address VARCHAR(30),"
                  f"total_slots INTEGER,"
                  #f" bikes VARCHAR(4),"
                  f"lat,"
                  f"lon,"
                  f"name VARCHAR(50),"
                  f"stationType VARCHAR(4),"
                  f"status VARCHAR(3))"
            )
            # table stations
            for st in self.data_json:
                  cur.execute("insert into stations values (?,?,?,?,?,?,?,?)",
                            [st['id'],
                             st['address'],
                             int(st['bikes']) + int(st['slots']),
                             st['lat'], st['lon'],
                             st['name'],
                             st['stationType'],
                             st['status']
                             ])
                  con.commit()

            # historiek tabel
            query = f"CREATE TABLE if not exists historiek (id INTEGER PRIMARY KEY, "
            for i in range(24):
                  query += f"H{i}_00 INTEGER,"
                  query += f"H{i}_30 INTEGER"
                  if i !=23:
                        query += ", "
            query += ")"
            cur.execute(query)
            for st in self.data_json:
                  print(st['id'])
                  cur.execute("insert into historiek (id) values(?)", [st['id']])
            #cur.execute("insert into historiek (id) values(1)")
            con.commit()
            #for st in self.data_json:

      def currTimefield(self):
            self.set_t()
            h = self.t.hour
            m = self.t.minute
            if m > 30:
                  field = f"H{h}_30"
            else:
                  field = f"H{h}_00"
            return field

      def registerData(self):
            self.read_json()
            con = sqlite3.connect("veloDatabase.db")
            cur = con.cursor()

            query = f'update historiek set H0_00 = 8 where id = 1'
            print(query)

            cur.execute(query)
            for st in self.data_json:
                  cur = con.cursor()
                  query = f'update historiek set {self.currTimefield()}={st["bikes"]} where id={st["id"]}'
                  cur.execute(query)
                  print(query)
            con.commit()
            con.close()

class StaticSiteGenerator:
      def __init__(self, db, htmlFile):
            self.db = db
            self.htmlFile = htmlFile

      def getTableData(self, table):
            con = sqlite3.connect(self.db)
            cur = con.cursor()
            query = f"Select * from {table}"
            res = cur.execute(query)
            return res

      def writeHTML(self, tableName, headerlist):
            f = open(self.htmlFile, "w", encoding="utf-8")  # read, write append

            with open("template.html", "r",encoding="utf-8") as template:
                  lines = template.readlines()
            for i in range(0,8):
                  f.write(lines[i])

            table = ""
            res = self.getTableData(tableName)
            table += "<table class='table'>\n"
            table += "\t<tr>\n"
            for item in headerlist:
                  table += f"\t\t<td>{item}</td>\n"
            table += "\t</tr>\n"

            for line in res:
                  table += "\t<tr>\n"
                  for item in line:
                        table += f"\t\t<th>{item}</th>\n"
                  table += "\t</tr>\n"

            table += "</table>\n"

            f.write(table)
            for i in range(9,11):
                  f.write(lines[i])
            f.close()




if __name__ == "__main__":
      App = VeloDatabaseCreator()
      #while True:
      #       App.set_t()
      #       print(f"{App.t.hour}:{App.t.minute}")
      #       App.setupDB()
      #       time.sleep(1*60)

      #App.setupDB()
      #print(App.currTimefield())
      App.registerData()

      stationsHeaders = ["ID", "address", "total_slots", "lat", "lon", "name", "stationType", "status"]
      historiekHeaders = ["ID"]
      for i in range(24):
            historiekHeaders.append(f"H{i}_00")
            historiekHeaders.append(f"H{i}_30")
      print(historiekHeaders)

      site = StaticSiteGenerator("veloDatabase.db", "historiek.html")
      site.writeHTML("historiek", historiekHeaders)
      site.htmlFile = "stations.html"
      site.writeHTML("stations", stationsHeaders)




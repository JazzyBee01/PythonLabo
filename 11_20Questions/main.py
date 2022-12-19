import dataclasses
from dataclasses import dataclass, asdict
import json
import random


@dataclass()
class Dier:
    naam: str
    klasse: str
    dieet: str
    aantalPoten: int
    oorsprong: str  # continent
    kleur: list
    gegeten: bool
    huisdier: bool
    huid: str
    pattroon: list
    habitat: list

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}

dierEigenschappen = {
    "klasse": ("zoogdier", "reptiel", "vis", "vogel", "amfibie", "insect", "anders"),
    "dieet": ("carnivoor", "herbivoor", "pescetarier", "insecteneter", "omnivoor", "anders"),
    "aantalPoten": (4,8,0,2,6, 100, 1000, "anders"),
    "kleur": ("bruin", "zwart", "wit", "grijs", "groen","rood", "oranje", "geel",  "blauw", "paars", "anders"),
    "gegeten": (True, False),
    "huisdier": (True, False),
    "huid" :("vacht", "veren", "schubben", "anders"),
    "pattroon":("vlekken", "strepen", "geen patroon", "anders"),
    "oorsprong": ("Europa", "Afrika", "Oceanie", "Azie", "Amerika", "anders"),
    "habitat": ("bos", "zee", "stad", "huis", "jungle", "anders")
}
tuplelist = ["kleur", "pattroon", "oorsprong"]
class App_20_Questions():

    def __init__(self):
        self.data = {}
        self.datainlezen()
        self.antwoorden = {}
        self.mogelijkeDieren = []
        self.aantalVragen = 0

        self.klasse = ""
        self.dieet = ""

        self.dierEigCopy = {}
        for eig in dierEigenschappen.keys():
            self.dierEigCopy[eig] = dierEigenschappen[eig]


    def datainlezen(self):
        with open('data.json') as json_file:
            self.data = json.load(json_file)

    def stel_vraag(self, tekst, criteria=None):
        if criteria is None:
            criteria = ["ja", "nee", "anders"]
        antw = ""
        while True:
            vraag = f"{self.aantalVragen+1}. {tekst} \n"
            for c in criteria:
                vraag += str(c) + "/"
            antw = input(vraag +": ")
            if antw == "True" or antw == "true":
                antw = True
            elif antw == "False" or antw == "false":
                antw = False
            if antw in criteria:
                break
            elif antw == "exit":
                exit()
            else:
                print('Ongeldig antwoord.')
        self.aantalVragen += 1
        return antw


    def vraag_eig_af(self,type_eigenschap):
        list = []
        for dier in self.mogelijkeDieren:
            if self.data[dier][type_eigenschap] not in list:
                list.append(self.data[dier][type_eigenschap])
        #print(list)
        # als tuppel, kies random

        #anders
        for eig in list:
            antw = self.stel_vraag(self.bepaal_vraag_vorm(type_eigenschap, eig))
            if antw == "ja":
                i = 0
                while i < len(self.mogelijkeDieren):
                    dier = self.mogelijkeDieren[i]
                    if eig not in self.data[dier][type_eigenschap]:
                        self.mogelijkeDieren.remove(self.data[dier]["naam"])
                        # Items verschuiven -> idex verminderen
                        i -= 1
                    i += 1
                #print(self.mogelijkeDieren)
                self.antwoorden[type_eigenschap] = eig
                self.elemineer(type_eigenschap, eig, "ja")
                break
            elif antw == "nee":
                # elimineer
                i = 0
                while i < len(self.mogelijkeDieren):
                    dier = self.mogelijkeDieren[i]
                    if str(eig) in self.data[dier][type_eigenschap]:
                        self.mogelijkeDieren.remove(self.data[dier]["naam"])
                        #Items verschuiven -> idex verminderen
                        i -= 1
                    i+=1
                #print(self.mogelijkeDieren)
                self.elemineer(type_eigenschap, eig, "nee")
            elif antw == "anders":
                break
            if len(self.mogelijkeDieren) < 2:
                break

    def vragen_op_basis_van_data(self):
        self.mogelijkeDieren = []
        for dier in self.data.keys():
            self.mogelijkeDieren.append(dier)

        #print(self.mogelijkeDieren)
        while len(self.mogelijkeDieren) > 1 and self.aantalVragen <= 19:
            self.vraag_eig_af("klasse")
            if len(self.mogelijkeDieren) > 1 and self.aantalVragen <= 19:
                self.vraag_eig_af("huisdier")
            if len(self.mogelijkeDieren) > 1 and self.aantalVragen <= 19:
                self.vraag_eig_af("dieet")
            if len(self.mogelijkeDieren) > 1 and self.aantalVragen <= 19:
                self.vraag_eig_af("aantalPoten")
            if len(self.mogelijkeDieren) > 1 and self.aantalVragen <= 19:
                self.vraag_eig_af("oorsprong")

        if len(self.mogelijkeDieren) == 1:
            antw = self.stel_vraag(f"is het een {self.mogelijkeDieren[0]}?")
            if antw == "ja":
                print(f"hoera, geraden in {self.aantalVragen}")
                exit()
            elif antw == "nee" and self.aantalVragen < 20:
                self.mogelijkeDieren.remove(self.mogelijkeDieren[0])

        if len(self.mogelijkeDieren) == 0:
            antw2 = self.stel_vraag("Dier niet gevonden :( \n mogen we je extra vragen stellen zodat we onze kennis kunnen bijwerken?")
            if antw2 == "ja":
                while True:
                    naam = input(f"Wat is de naam van het dier dan?\n:")
                    if len(naam.split()) == 1:
                        break
                    else:
                        print('Ongeldig antwoord. Geef 1 woord op')
                if naam not in self.data.keys():
                    self.wilde_vragen(randomised=False)
                    self.check_en_registreer(naam)
                else:
                    print("Dier staat al in ons systeem. Bedankt voor je deelname")
                    exit()
            else:
                print("Jammer, tot de volgende keer!")
                exit()

        if len(self.mogelijkeDieren) < 1:
            self.wilde_vragen(True)



    def check_en_registreer(self, naam):
        print("checken en registreren")
        print("----------------------")
        print('\t{:12}:  '.format("naam"), end="")
        print(naam)
        for eig in self.dierEigCopy:
            print('\t{:12}:  '.format(eig),end = "")
            if type(self.dierEigCopy[eig]) == str:
                print(self.dierEigCopy[eig], end="")
            else:
                for waarde in self.dierEigCopy[eig]:
                    print(waarde, end=" ")
            print()

        antw = self.stel_vraag("is bovenstaande informatie correct?")
        while antw != "ja":
            incorrecte_eigenschap = self.stel_vraag("Welke informatie is niet correct?", self.dierEigCopy)
            waarde = ""
            waarde = self.stel_vraag(f"Wat moet {incorrecte_eigenschap} dan wel zijn?", dierEigenschappen[incorrecte_eigenschap] )
            self.dierEigCopy[incorrecte_eigenschap] = (waarde,)
            for eig in self.dierEigCopy:
                print('\t{:12}:  '.format(eig), end="")
                for waarde in self.dierEigCopy[eig]:
                    print(f"{waarde}", end=" ")
                print()

            antw = self.stel_vraag("is bovenstaande informatie correct?")

        dier = {"naam": naam}
        for eig in self.dierEigCopy:
            if eig in tuplelist:
                #dier[eig] = self.dierEigCopy[eig]
                dier[eig] = tuple(str(item) for item in self.dierEigCopy[eig])

            else:
                dier[eig] = str(self.dierEigCopy[eig][0])

        #print(dier)
        self.data[naam] = dier
        f = open("data.json", "w")
        json.dump(self.data, f, indent = 4)
        f.close()


    def bepaal_vraag_vorm(self, eig, waarde):
        if eig in ("klasse", "dieet", "naam"):
            str = f"Is het een {waarde}?"
        elif eig == "kleur":
            str = f"Is het {waarde}?"
        elif eig in ("huid", "pattroon"):
            str = f"Heeft het {waarde}?"
        elif eig == "oorsprong":
            str = f"Komt het dier oorspronkelijk van {waarde}?"
        elif eig == "aantalPoten":
            str = f"Heeft het {waarde} poten?"
        elif eig == "habitat":
            str = f"Woont het in een {waarde}?"
        elif eig == "gegeten":
            str = f"Wordt het gegeten?"
        elif eig == "huisdier":
                str = f"Kan het als huisdier worden gehouden? {waarde}"
        else:
            str = "eigenschap niet herkend"
        return str
    
    def randomkey(self, dict):
        keylist = []
        for key in dict.keys():
            keylist.append(key)
        return random.choice(keylist)

    def wilde_vragen(self, randomised=True):
        if randomised == True:
            while self.aantalVragen < 19:
                eigenschap = self.randomkey(self.dierEigCopy)
                while len(self.dierEigCopy[eigenschap]) <= 1:
                    eigenschap = self.randomkey(self.dierEigCopy)
                waarde = ""
                while waarde in ("", "geen", "False","anders", False, 'false'):
                    waarde = random.choice(self.dierEigCopy[eigenschap])
                str = self.bepaal_vraag_vorm(eigenschap, waarde)
                antw = self.stel_vraag(str)
                self.elemineer(eigenschap, waarde, antw)
                if self.aantalVragen >= 19:
                    break
        elif randomised == False:
            for eig in self.dierEigCopy:
                if len(self.dierEigCopy[eig]) > 1:
                     for waarde in self.dierEigCopy[eig]:
                         if waarde not in ("", "geen", False,"anders"):
                            antw = self.stel_vraag(self.bepaal_vraag_vorm(eig, waarde))
                            self.elemineer(eig, waarde, antw)
                            if antw == "ja" and eig not in ["pattroon", "habitat"]:
                                break
            print(self.dierEigCopy)

    def elemineer(self, eigenschap, waarde, antw):
        if antw == "ja":
            self.antwoorden[eigenschap] = waarde
            self.dierEigCopy[eigenschap] = (waarde,)
            # hou bij
        elif antw == "nee":
            new_tuple_1 = tuple(item for item in self.dierEigCopy[eigenschap] if str(item) != str(waarde))
            self.dierEigCopy[eigenschap] = new_tuple_1
            # probeer met andere waarde

    def resetBasisData(self):
        data = {}
        kat = Dier(naam = "kat",
                   klasse = "zoogdier",
                   dieet="carnivoor",
                   aantalPoten=4,
                   oorsprong = "europa",
                   kleur = ["zwart", "wit", "grijs", "bruin" "oranje"],
                   gegeten=False,
                   huisdier=True,
                   huid="vacht",
                   pattroon=["vlekken", "strepen", "geen"],
                   habitat=["huis"])
        data["kat"] = kat.dict()
        hond = Dier(naam="hond",
                    klasse="zoogdier",
                    dieet="carnivoor",
                    aantalPoten=4,
                    oorsprong="onbekend",
                    kleur=["zwart", "wit", "grijs", "bruin"],
                    gegeten=False,
                    huisdier=True,
                    huid="vacht",
                    pattroon=["bevlekt", "geen"],
                    habitat=["huis"])
        data["hond"] = hond.dict()
        spin = Dier(naam="spin",
                    klasse="insect",
                    dieet="insecteneter",
                    aantalPoten=8,
                    oorsprong="onbekend",
                    kleur=["zwart", "wit", "grijs", "bruin", "rood", "blauw"],
                    gegeten=False,
                    huisdier=False,
                    huid="geen",
                    pattroon=["geen"],
                    habitat=["anders"])
        data["spin"] = spin.dict()
        zeehond = Dier(naam="zeehond",
                       klasse="zoogdier",
                       dieet="viseter",
                       aantalPoten=0,
                       oorsprong="onbekend",
                       kleur=["grijs"],
                       gegeten=False,
                       huisdier=False,
                       huid="geen",
                       pattroon=["geen"],
                       habitat=["zee"])
        data["zeehond"] = zeehond.dict()

        with open('data.json', 'w') as fp:
            json.dump(data, fp, indent=4)

    def dict(self):
        return {k: v for k, v in asdict(self).items()}

def main():
    app = App_20_Questions()
    #app.resetBasisData()
    app.vragen_op_basis_van_data()
    #app.dierEigCopy = {'klasse': ('zoogdier',), 'dieet': ('herbivoor',), 'aantalPoten': (4,), 'kleur': ('grijs',), 'gegeten': (False,), 'huisdier': (False,), 'huid': ('vacht',), 'pattroon': ('strepen',), 'oorsprong': ('Europa',)}
    #app.check_en_registreer("kat")

if __name__ == '__main__':
    main()

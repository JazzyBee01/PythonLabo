import json
import sys

def readlists():
    global tasks
    global completed
    try:
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        print('geen tasks gevonden')
        tasks = []
        pass
    try:
        with open("completed.json","r") as f:
            completed = json.load(f)
    except FileNotFoundError:
        print('geen log file gevonden')
        completed = []
        pass

def savelists():
    with open("tasks.json", "w") as f:
            json.dump(tasks, f)
    with open("completed.json","w") as f:
            json.dump(completed, f)

def useMenu():
    menu = '1. Toon taken\n2. Voltooi taak\n3. Voeg taak toe\n4. Verwijder taak\n 5. Toon voltooid'
    print(menu)

    keuze = int(input('kies een optie (1/2/3/4/5): '))
    while keuze not in {1,2,3,4,5}:
        print('Geen geldige keuze')
        keuze = int(input('kies een optie (1/2/3/4/5): '))
    
def show(lijst):
    ...
        

def main():
    '''
    if no arguments are provided, you will be guided by a menu
    '''
    readlists()

    
    #check op systeemargumenten
    if len(sys.argv) > 1:
        print('sys arg found')
        
    #als geen systeem argumenten -> vragen stellen
    else:
        print ('no sys arg found')
        useMenu()
    savelists()

if __name__ == "__main__":
    main()
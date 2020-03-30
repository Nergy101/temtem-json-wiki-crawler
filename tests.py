import json
temtems = []

with open('temtem.json') as jsonFile:
    temtems = json.load(jsonFile)


def find(temtemName):
    for temtem in temtems:
        if temtem['Name'] == temtemName:
            return temtem;


def printInfo(temtem):
    print(temtem)

# find temtem with evlution-chain of 3
for currentTemtem in temtems:
    try:
        evolvesFrom = currentTemtem['General']['EvolvesFrom']
        evolvesTo = currentTemtem['General']['EvolvesTo']
        if evolvesFrom and evolvesTo:
            printInfo(find(evolvesFrom))
            printInfo(currentTemtem)
            printInfo(find(evolvesTo))
            print('----------')
    except:
        pass

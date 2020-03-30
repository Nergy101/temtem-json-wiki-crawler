import csv
import json
import time

import requests
from bs4 import BeautifulSoup

from temtemCollector import getTemtemTechniquesList, getTemtemLocationsList, getTemtemPersonality, getTemtemTraits

start_time = time.time()

# from CSV
temtems = []
with open('temtems.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=' ')
    for row in reader:
        temtem = {}
        temtemName = row['Temtem']
        # print('creating', temtemName)
        URL = f'https://temtem.gamepedia.com/{temtemName}'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            temtem['Name'] = temtemName

            try:
                temtem['General'] = {}
                temtem['General']['No'] = row['No']
                temtem['General']['EvolveInfo'] = soup.find('b', text=temtemName).findParent('p').text.strip()

                try:
                    temtem['General']['EvolvesFrom'] = soup.find('b', text='Evolves from').findParent('tr') \
                        .find('td').text.strip()
                except:
                    pass
                try:
                    temtem['General']['EvolvesTo'] = soup.find('b', text='Evolves to').findParent('tr') \
                        .find('td').text.strip()
                except:
                    pass


                temtem['General']['Types'] = {
                    'Type1': row['Type1'],
                    'Type2': row['Type2'],
                }
            except Exception as e:
                print(e)
                print(f'couldn\'t get general info of {temtemName}')

            temtem['Appearance'] = {}
            try:
                temtem['Appearance']['AppearanceAndPersonality'] = getTemtemPersonality(soup)
                temtem['Appearance']['NormalImage'] = soup.find('img', alt=f'{temtemName}.png')['src'].strip()
                temtem['Appearance']['LumaImage'] = soup.find('img', alt=f'Luma{temtemName}.png')['src'].strip()
            except:
                print(f'couldn\'t get appearance info of {temtemName}')

            temtem['BaseStats'] = {
                'HP': row['HP'],
                'STA': row['STA'],
                'SPD': row['SPD'],
                'ATK': row['ATK'],
                'DEF': row['DEF'],
                'SPATK': row['SPATK'],
                'SPDEF': row['SPDEF'],
                'Total': row['Total']}

            temtem['Physical'] = {}
            temtem['Physical']['Height'] = soup.find('b', text='Height').findParent('tbody').find('td').text.strip()
            temtem['Physical']['Weight'] = soup.find('b', text='Weight').findParent('tbody').find('td').text.strip()

            temtem['Technical'] = {}
            temtem['Technical']['MaleRatio'] = soup.find('b', text='Gender Ratio').findParent('tr').find('td').text[0:2]
            temtem['Technical']['CatchRate'] = soup.find('b', text='Catch Rate').findParent('tr').find('td').text

            try:
                temtem['Technical']['Traits'] = getTemtemTraits(soup)
            except:
                print(f'couldn\'t get traits info of {temtemName}')
            try:
                temtem['Techniques'] = getTemtemTechniquesList(soup)
            except:
                print(f'couldn\'t get techniques info of {temtemName}')
            try:
                temtem['Locations'] = getTemtemLocationsList(soup, temtemName)
            except:
                print(f'couldn\'t get locations info of {temtemName}')

            temtems.append(temtem)
        except Exception as e:
            print(e)
            print(f'couldn\'t get unknown info of {temtemName}')

# save to JSON
with open('temtem.json', 'w') as jsonFile:
    jsonFile.write(json.dumps(temtems, indent=4).replace(r'\n', ''))

# print(json.dumps(temtems, indent=4))
elapsed_time = time.time() - start_time
print(elapsed_time)
print('Temtem JSON Done!')


#  TODO characters JSON

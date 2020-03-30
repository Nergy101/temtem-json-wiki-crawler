import re


def getTemtemTechniquesList(soup):
    techniquesTBody = soup.find("caption", text=re.compile('^List of Techniques')).findParent("table").find("tbody")
    techniquesList = [[cell.text for cell in row.findAll("td")] for row in techniquesTBody.findAll("tr")]

    techniquesListTypesClassPriority = [[cell['alt'] for cell in row.findAll("img")]
                                        for row in techniquesTBody.findAll("tr")]

    for list in techniquesListTypesClassPriority:
        if len(list) == 3:
            list.insert(1, "-")

    for index, techniques in enumerate(techniquesList):
        techniques.extend(techniquesListTypesClassPriority[index])
        # print(techniques)

    techniquesDict = {}
    for technique in techniquesList:
        try:
            techniquesDict[technique[1]] = technique
        except:
            pass

    # print(techniquesDict)

    techs = []
    for techlist in techniquesDict:
        tech = {'Lvl': techniquesDict[techlist][0], 'Name': techniquesDict[techlist][1],
                'Damage': techniquesDict[techlist][4], 'Stamina': techniquesDict[techlist][5],
                'Hold': techniquesDict[techlist][6], 'Type1': techniquesDict[techlist][8],
                'Type2': techniquesDict[techlist][9], 'Class': techniquesDict[techlist][10],
                'Priority': techniquesDict[techlist][11]}
        techs.append(tech)
    return techs


def getTemtemLocationsList(soup, temtemName: str = "Kaku"):
    locationsTBody = soup.find(text=f'Islands, Routes and Landmarks where you can find {temtemName}') \
        .findParent('table').find('tbody')

    locationLists = [[cell.text for cell in row.findAll("td")] for row in locationsTBody.findAll("tr")]

    locations = []
    for locationList in locationLists:
        try:
            location = {"Route/Landmark": locationList[0], "Island": locationList[1],
                        "Rarity": locationList[2], "Level": locationList[3]}
            locations.append(location)
        except:
            pass
    return locations


def getTemtemTraits(soup):
    traits = []
    for link in soup.find('b', text="Traits").findParent('th').findParent('tr').find('td').findAll('a'):
        traits.append(link.text)
    return traits


def getTemtemPersonality(soup):
    personalityParagraph1 = soup.find("span", id='Appearance_&_Personality').findParent("h2").findNext('p')
    personalityParagraph2 = soup.find("span", id='Appearance_&_Personality').findParent("h2") \
        .findNext('p').findNext('p')
    return personalityParagraph1.text + personalityParagraph2.text

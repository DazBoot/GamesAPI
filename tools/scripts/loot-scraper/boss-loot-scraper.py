import csv
import os
import re
import sys
import xml.etree.ElementTree as ET

import requests

def getItemData(itemId):
  itemXMLData = requests.get('https://www.wowhead.com/item=' + itemId + '&xml')
  return itemXMLData.content;

def getItemName(itemId):
  itemData = getItemData(itemId)
  root = ET.fromstring(itemData)
  return root[0][0].text

def printBossItems(itemIds):
  for itemId in itemIds:
    itemXMLData = requests.get('https://www.wowhead.com/item=' + itemId + '&xml')
    print('   * ' + getItemName(itemId) + ' (' + itemId + ')')

def getBossLootTable(bossPageUrl):
  page = requests.get(bossPageUrl);
  if(page.status_code != 200):
    trace('Unable to download data from ' + bossPageUrl)
    trace('Recieved error code: ' + page.status_code)
    return

  tableRegex = r"WH.Gatherer.addData\(([0-9]+), ([0-9]+), (.*?)\)"
  tableMatches = re.findall(tableRegex, str(page.content))
    
  itemIdRegex = r'([0-9]+)":{'
  tableStr = ''
  for match in tableMatches:
    tableFound = False
    if not tableFound and match[0] == '3':
      tableStr = match[2]
      tableFound = True
      
  return re.findall(itemIdRegex, tableStr)

def getInstancesFromCSV(filePath):
  with open(filePath, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    result = []
    for row in reader:
      instance = {}
      instance['name'] = row[0]
      instance['bosses'] = []
      for encounter in row[1:]:
        if encounter != '""':
          instance['bosses'].append([value.strip() for value in encounter.strip('"').split('-')])
      result.append(instance)
    csvfile.close()
    return result

def writeLootDataToCSV(directory, instance):
  fileName = instance['name'].replace(' ', '-') + '.csv'
  with open(directory + fileName, 'w') as outputFile:
    for boss in instance['bosses']:
      line = boss[0] + ','
      print(boss)
      line += ','.join(getBossLootTable(boss[1]))
      outputFile.write(line + '\n')
  return fileName
    

if __name__ == '__main__':
  #If we have no arguments, prompt the user for a boss encounter ID
  if len(sys.argv) == 1:
    bossPageURL = input('Please enter a WoWHead boss NPC page URL to scrape: ')
    lootItems = getBossLootTable(bossPageURL)
    print('\n' + str(len(lootItems)) + ' Loot Items Found:')
    printBossItems(lootItems)
    print('')

  #If we have one argument, assume it in an input csv file
  elif len(sys.argv) == 2:
    if not os.path.exists(sys.argv[1]):
      print('Could not find file: ' + sys.argv[1])
    else:
      instances = getInstancesFromCSV(sys.argv[1])
      for instance in instances:
        for bossData in instance['bosses']:
          lootItems = getBossLootTable(bossData[1])
          print(bossData[0] + ' - ' + str(len(lootItems)) + ' items')
          printBossItems(lootItems)
          print('')
    
    #If we have two arguments, use an input and an output file
  elif len(sys.argv) == 3:
    if not os.path.exists(sys.argv[1]):
      print('Could not find file: ' + sys.argv[1])
    else:
      instances = getInstancesFromCSV(sys.argv[1])
      directory = sys.argv[2]
      if not os.path.exists(directory):
        os.makedirs(directory)
      for instance in instances:
        fileName = writeLootDataToCSV(directory, instance)
        print('Wrote data file for ' + instance['name'] + ' to ' + fileName)



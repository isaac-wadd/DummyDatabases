
import random as r, os, json
from pathlib import Path
from string import ascii_lowercase, ascii_uppercase, digits
from .models import *
from datetime import datetime, timedelta

ALPHA_HEX_LOWER = 'abcdef'
ALPHA_HEX_UPPER = 'ABCDEF'
MISC_CHARS = '!@#$%^&*()-_=+`~[{}]|:;,<.>/?'
BASE_DIR = Path(__file__).resolve().parent.parent

# basic file path getter for general use

def getFilePath(fileName):
    filePartPath = f'dataFiles/{fileName}'
    return os.path.join(os.path.join(BASE_DIR, filePartPath))

# generates random string data

def genRandomStringData(options, rowCount):
    data = []
    choiceStr = ''
    opts = options['randomOptions']
    if opts['includes']['alpha']['hexOnly']:
        if opts['includes']['alpha']['lower']:
            choiceStr += ALPHA_HEX_LOWER
        if opts['includes']['alpha']['upper']:
            choiceStr += ALPHA_HEX_UPPER
    else:
        if opts['includes']['alpha']['lower']:
            choiceStr += ascii_lowercase
        if opts['includes']['alpha']['upper']:
            choiceStr += ascii_uppercase
    if opts['includes']['numeric']:
        choiceStr += digits
    if opts['includes']['misc']:
        choiceStr += MISC_CHARS
    randLenMin = opts['length']['min']
    randLenMax = opts['length']['max'] + 1
    for _ in range(rowCount):
        randLen = r.randrange(randLenMin, randLenMax)
        newDatum = ''
        for _ in range(randLen):
            newDatum += r.choice(choiceStr)
        data.append(newDatum)
    return data

# generates first names data

def genFirstNamesData(includes, rowCount, strCase):
    match includes:
        case (True, True):
            fileName = 'allFirstNames.json'
        case (True, False):
            fileName = 'femaleFirstNames.json'
        case (False, True):
            fileName = 'maleFirstNames.json'
        case _:
            fileName = 'allFirstNames.json'
    file = open(getFilePath(fileName), 'r')
    content = json.load(file)
    file.close()
    match strCase:
        case 'lower':
            content = [ name.lower() for name in content ]
        case 'upper':
            content = [ name.upper() for name in content ]
    return [ r.choice(content) for _ in range(rowCount) ]

# generates data for string field

def genStringData(options, rowCount):
    data = []
    if options['random']:
        data = genRandomStringData(options, rowCount)
    elif options['firstNames']:
        includes = (options['firstNamesOptions']['female'], options['firstNamesOptions']['male'])
        data = genFirstNamesData(includes, rowCount, options['firstNamesOptions']['case'])
    # elif options['lastNames']:
    # elif options['countries']:
    # elif options['phoneNumbers']:
    return data

# generates random integer, float and date data

def genIntData(options, rowCount):
    data = []
    for _ in range(rowCount):
        newDatum = r.randint(options['min'], options['max'])
        data.append(newDatum)
    return data

def genFloatData(options, rowCount):
    data = []
    for _ in range(rowCount):
        newDatum = round(r.uniform(options['min'], options['max']), options['precision'])
        data.append(newDatum)
    return data

def getRandomDate(minDate, maxDate):
    delta = maxDate - minDate
    deltaSeconds = int(delta.total_seconds())
    seconds = r.randrange(deltaSeconds)
    return minDate + timedelta(seconds=seconds)

def genDateData(options, rowCount):
    data = []
    for _ in range(rowCount):
        minDate = datetime.fromtimestamp(options['minDate'])
        maxDate = datetime.fromtimestamp(options['maxDate'])
        newDatum = getRandomDate(minDate, maxDate)
        data.append(newDatum)
    return data

# generates table data for each field using above functions except genAssociationData

def genTableData(table):
    fieldsData = {}
    for field in Field.objects.filter(table=table):
        match field.dataType:
            case 'TEXT':
                fieldsData.update({field.name: genStringData(field.options, table.rowCount)})
            case 'INTEGER':
                fieldsData.update({field.name: genIntData(field.options, table.rowCount)})
            case 'REAL':
                fieldsData.update({field.name: genFloatData(field.options, table.rowCount)})
            case 'DATETIME':
                fieldsData.update({field.name: genDateData(field.options, table.rowCount)})
            case _:
                fieldsData.update({field.name: genStringData(field.options, table.rowCount)})
    return fieldsData

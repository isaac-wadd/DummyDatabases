
from .models import *

# creates options object for string field

def getStringFieldOptions(postData):
    options = Field.getDefaultStringOptions()
    match postData.get('stringDataOptions'):
        case 'stringRandom':
            options['random'] = True
            if postData.get('length'):
                options['randomOptions']['length']['max'] = int(postData.get('maxLength'))
                options['randomOptions']['length']['min'] = int(postData.get('minLength'))
            if postData.get('alpha'):
                if postData.get('upper'):
                    options['randomOptions']['includes']['alpha']['upper'] = True
                if postData.get('lower'):
                    options['randomOptions']['includes']['alpha']['lower'] = True
                if postData.get('hexOnly'):
                    options['randomOptions']['includes']['alpha']['hexOnly'] = True
            if postData.get('numeric'):
                options['randomOptions']['includes']['numeric'] = True
            if postData.get('misc'):
                options['randomOptions']['includes']['misc'] = True
        case 'firstNames':
            options['firstNames'] = True
            options['firstNamesOptions']['case'] = postData.get('firstNamesCase')
            if not postData.get('female'):
                options['firstNamesOptions']['female'] = False
            if not postData.get('male'):
                options['firstNamesOptions']['male'] = False
        case 'lastNames':
            options['lastNames'] = True
            options['lastNamesOptions']['case'] = postData.get('lastNamesCase')
        case 'countries':
            options['countries'] = True
            options['countriesOptions']['case'] = postData.get('countriesCase')
        case 'phoneNumbers':
            options['phoneNumbers'] = True
            if postData.get('areaCode'):
                options['phoneNumbersOptions']['areaCode'] = True
    return options

# creates options object for integer field

def getIntFieldOptions(postData):
    options = Field.getDefaultIntOptions()
    if postData.get('intMin'):
        options['min'] = int(postData.get('intMin'))
    if postData.get('intMax'):
        options['max'] = int(postData.get('intMax'))
    if postData.get('intAvg'):
        options['average'] = int(postData.get('intAvg'))
    return options

# creates options object for float field

def getFloatFieldOptions(postData):
    options = Field.getDefaultFloatOptions()
    if postData.get('precision'):
        options['precision'] = int(postData.get('precision'))
    if postData.get('floatMin'):
        options['min'] = float(postData.get('floatMin'))
    if postData.get('floatMax'):
        options['max'] = float(postData.get('floatMax'))
    if postData.get('floatAvg'):
        options['average'] = float(postData.get('floatAvg'))
    return options

# creates options object for datetime field

def getDateTimeFieldOptions(postData):
    options = Field.getDefaultDateTimeOptions()
    if postData.get('includeTime'):
        options['includeTime'] = True
    if postData.get('minDate'):
        options['minDate'] = datetime.timestamp(datetime.strptime(postData.get('minDate'), '%Y-%m-%d'))
    if postData.get('maxDate'):
        options['maxDate'] = datetime.timestamp(datetime.strptime(postData.get('maxDate'), '%Y-%m-%d'))
    return options

# creates and returns options based on type of field

def getFieldOptions(fieldType, post):
    match fieldType:
        case 'TEXT':
            return getStringFieldOptions(post)
        case 'INTEGER':
            return getIntFieldOptions(post)
        case 'REAL':
            return getFloatFieldOptions(post)
        case 'DATETIME':
            return getDateTimeFieldOptions(post)
        case _:
            return getStringFieldOptions(post)


from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Schema(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'schema'

class Table(models.Model):
    name = models.CharField(max_length=30)
    rowCount = models.IntegerField(default=50)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'table'

class Field(models.Model):
    dataTypes = {
        'TEXT': 'string',
        'INTEGER': 'integer',
        'REAL': 'decimal',
        'DATETIME': 'date/time'
    }

    def getDefaultStringOptions():
        return {
            'firstNames': False,
            'firstNamesOptions': {
                'case': 'title',
                'female': True,
                'male': True
            },
            'lastNames': False,
            'lastNamesOptions': {
                'case': 'title'
            },
            'countries': False,
            'countriesOptions': {
                'case': 'names'
            },
            'phoneNumbers': False,
            'phoneNumbersOptions': {
                'areaCode': False
            },
            'random': False,
            'randomOptions': {
                'length': {
                    'min': 1,
                    'max': 8
                },
                'includes': {
                    'alpha': {
                        'upper': False,
                        'lower': False,
                        'hexOnly': False
                    },
                    'numeric': False,
                    'misc': False
                }
            }
        }

    def getDefaultIntOptions():
        return {
            'min': 20,
            'max': 100,
            'average': 60
        }

    def getDefaultFloatOptions():
        return {
            'precision': 2,
            'min': 20,
            'max': 100,
            'average': 60
        }

    def getDefaultDateTimeOptions():
        return {
            'includeTime': False,
            'minDate': datetime.timestamp(datetime.now()),
            'maxDate': datetime.timestamp(datetime.now())
        }

    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True)
    dataType = models.CharField(max_length=8, default='TEXT')
    name = models.CharField(max_length=30)
    options = models.JSONField(default=getDefaultStringOptions)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'field'

class Association(models.Model):
    types = {
        1: 'one to one',
        2: 'one to many',
        3: 'many to many'
    }
    type = models.CharField(max_length=12, default=types.get(2))
    rowCount = models.IntegerField(default=50, null=True)
    table1 = models.ForeignKey(Table, related_name='table1', on_delete=models.CASCADE, null=True)
    table2 = models.ForeignKey(Table, related_name='table2', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'association'

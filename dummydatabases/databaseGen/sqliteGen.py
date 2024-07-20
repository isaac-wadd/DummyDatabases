
import os, sqlite3, random as r
from .models import *
from datetime import datetime
from django.conf import settings

# makes new file and stores sql script inside

def genSqlFile(schema, statement):
    filePath = os.path.join(settings.MEDIA_ROOT, f'{schema.name}.sql')
    with open(filePath, 'w+') as sqlFile:
        sqlFile.write(statement)
        sqlFile.close()

# executes the sql script to new sqlite file

def writeAll(schema, statement):
    filePath = os.path.join(settings.MEDIA_ROOT, f'{schema.name}.sqlite3')
    open(filePath, 'w+').close()
    con = sqlite3.connect(filePath)
    cur = con.cursor()
    cur.executescript(statement)
    cur.close()
    con.close()

# orders tables in a consumable manner for the sql to execute properly

def getOrderedTableList(schema):
    tables = []
    for table in Table.objects.filter(schema=schema):
        association = Association.objects.filter(table2=table).exclude(type='many to many')
        if len(association):
            tables.append(table)
        else:
            tables.insert(0, table)
    return tables

# structures association tables for sqlite database, used in 'genDbStructure'

def genAssociationStructure(schema):
    statement = ''
    for table in Table.objects.filter(schema=schema):
        for association in Association.objects.filter(table1=table, type='many to many'):
            statement += f'CREATE TABLE {table.name}_{association.table2.name} (\n\t'
            statement += f'id INTEGER PRIMARY KEY,\n\t'
            statement += f'{table.name}_id INTEGER,\n\t'
            statement += f'{association.table2.name}_id INTEGER,\n\t'
            statement += f'FOREIGN KEY ({table.name}_id) REFERENCES {table.name}(id),\n\t'
            statement += f'FOREIGN KEY ({association.table2.name}_id) REFERENCES {association.table2.name}(id)\n);\n\n'
    return statement

# structures basic database using script string

def genDbStructure(schema):
    statement = ''
    for table in getOrderedTableList(schema):
        fieldsStr = 'id INTEGER PRIMARY KEY,\n\t'
        for field in Field.objects.filter(table=table):
            fieldsStr += f'{field.name} '
            if field.dataType == 'DATETIME':
                fieldsStr += 'TEXT,\n\t'
            else:
                fieldsStr += f'{field.dataType},\n\t'
        for association in Association.objects.filter(table2=table, type='one to many'):
            fieldsStr += f'{association.table1.name}_id INTEGER,\n\t'
            fieldsStr += f'FOREIGN KEY({association.table1.name}_id) REFERENCES {association.table1.name}(id),\n\t'
        fieldsStr = f'{fieldsStr[:-3]}\n'
        statement += f'CREATE TABLE {table.name} (\n\t{fieldsStr});\n\n'
    statement += genAssociationStructure(schema)
    return statement

# writes query and data for associations, randomly

def genAssociationData(schema):
    statement = ''
    manyToMany = False
    for table in Table.objects.filter(schema=schema):
        for association in Association.objects.filter(table1=table, type='many to many'):
            manyToMany = True
            statement += f'INSERT INTO {table.name}_{association.table2.name} ({table.name}_id, {association.table2.name}_id) VALUES\n\t'
            for rw in range(association.rowCount):
                statement += f'({r.randint(1, table.rowCount)}, {r.choice(range(1, association.table2.rowCount + 1))}),\n\t'
        if manyToMany:
            statement = f'{statement[:-3]};\n\n'
        for association in Association.objects.filter(table2=table, type='one to many'):
            for rw in range(1, table.rowCount + 1):
                statement += f'UPDATE {table.name} SET {association.table1.name}_id = {r.randint(1, association.table1.rowCount)} WHERE id = {rw};\n'
    return statement

# writes query to send data to database (only random for now)

def genDbData(schema, data):
    statement = ''
    for tableName, tableData in data.items():
        subStatement = f'INSERT INTO {tableName} ('
        fieldsStr = ''
        fieldData = []
        for fieldName, fieldDatum in tableData.items():
            fieldsStr += f'{fieldName}, '
            fieldData.append(fieldDatum)
        fieldsStr = f'{fieldsStr[:-2]})'
        valuesStr = ' VALUES\n'
        for indx in range(len(fieldData[0])):
            newData = [ d[indx] for d in fieldData ]
            values = ''
            for value in newData:
                if type(value).__name__ == 'str' or type(value).__name__ == 'datetime':
                    if str(type(value)) == '<class \'datetime.datetime\'>':
                        value = datetime.date(value)
                    values += f'\'{value}\', '
                elif type(value).__name__ == 'int' or type(value).__name__ == 'float':
                    values += f'{value}, '
                else:
                    values += f'\'{value}\', '
            values = values[:-2]
            valuesStr += f'\t({values}),\n'
        valuesStr = f'{valuesStr[:-2]};\n\n'
        subStatement += fieldsStr
        subStatement += valuesStr
        statement += subStatement
    statement += genAssociationData(schema)
    return statement

# uses above functions to create new file with given structure and data

def generateSqliteFile(schema, tableData, fileType):
    statement = genDbStructure(schema)
    statement += genDbData(schema, tableData)
    if fileType == 'sqlite3':
        writeAll(schema, statement)
    elif fileType == 'sql':
        genSqlFile(schema, statement)
    else:
        writeAll(schema, statement)


import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .validations import *
from .fieldOptions import getFieldOptions
from .dataGen import genTableData
from .databaseGen import generateFile
from django.conf import settings
from django.http import HttpResponse, Http404

# COMMON VIEWS ------------------------------------------------------------------------------------------

def homeView(req):
    res = render(req, 'dummydatabases/index.html')
    return res

@login_required(login_url='/login')
def schemasView(req):
    schemaDetails = []
    for schema in Schema.objects.filter(user=req.user):
        schemaDetails.append({
            'id': schema.id,
            'name': schema.name,
            'tables': Table.objects.filter(schema=schema).count()
        })
    ctxt = {
        'schemaDetails': schemaDetails
    }
    res = render(req, 'dummydatabases/schemas.html', ctxt)
    res.delete_cookie('currentSchema')
    res.delete_cookie('currentTable')
    return res

# REGISTRATION, LOGIN AND LOGOUT ------------------------------------------------------------------------------------------

def registerView(req):
    if req.method == 'POST':
        form = RegistrationForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            res = redirect('/schemas')
            return res
    else:
        form = RegistrationForm()
        ctxt = {
            'form': form
        }
        res = render(req, 'dummydatabases/register.html', ctxt)
        return res

def loginView(req):
    if req.method == 'POST':
        form = AuthenticationForm(req, data=req.POST)
        if form.is_valid():
            user = authenticate(req, username=req.POST.get('username'), password=req.POST.get('password'))
            login(req, user)
            res = redirect('/schemas')
            return res
        else:
            raise ValidationError('invalid credentials', code='invalid credentials')
    else:
        form = AuthenticationForm()
        ctxt = {
            'form': form
        }
        res = render(req, 'dummydatabases/login.html', ctxt)
        return res

def logoutView(req):
    logout(req)
    res = redirect('/login')
    res.delete_cookie('currentSchema')
    res.delete_cookie('currentTable')
    res.delete_cookie('userShowConfirm')
    return res

# SCHEMA CRUD ------------------------------------------------------------------------------------------

@login_required(login_url='/login')
def editSchema(req):
    isNew = False
    if req.POST.get('isNew') == 'true':
        schema = Schema()
        schema.user = req.user
        schema.save()
        isNew = True
    elif req.POST.get('isNew') == 'false':
        schema = Schema.objects.get(id=int(req.POST.get('schemaId')))
    else:
        schema = Schema.objects.get(id=int(req.COOKIES.get('currentSchema')))
    tables = Table.objects.filter(schema=schema)
    tableDetails = []
    for table in tables:
        tableDetails.append({
            'id': table.id,
            'name': table.name,
            'rowCount': table.rowCount,
            'fields': Field.objects.filter(table=table).count(),
            'associations': Association.objects.filter(table1=table).count() + Association.objects.filter(table2=table).count()
        })
    ctxt = {
        'schema': schema,
        'tableDetails': tableDetails,
        'isNew': isNew
    }
    res = render(req, 'dummydatabases/editSchema.html', ctxt)
    res.set_cookie('currentSchema', schema.id)
    return res

@login_required(login_url='/login')
def removeSchema(req):
    schema = Schema.objects.get(id=int(req.POST.get('schemaId')))
    schema.delete()
    res = redirect('/schemas')
    return res

@login_required(login_url='/login')
def saveSchema(req):
    schema = Schema.objects.get(id=int(req.POST.get('schemaId')))
    if schema.name != req.POST.get('name'):
        schema.name = req.POST.get('name')
    schema.save()
    return schemasView(req)

# TABLE CRUD ------------------------------------------------------------------------------------------

@login_required(login_url='/login')
def editTable(req):
    isNew = False
    schema = Schema.objects.get(id=int(req.COOKIES.get('currentSchema')))
    if req.POST.get('isNew') == 'true':
        table = Table()
        table.name = 'table_name'
        table.save()
        associations = []
        fields = []
        isNew = True
    else:
        if req.POST.get('isNew') == 'false':
            table = Table.objects.get(id=int(req.POST.get('tableId')))
        elif req.POST.get('isNew') == None:
            table = Table.objects.get(id=int(req.COOKIES.get('currentTable')))
        associations = Association.objects.filter(table1=table) | Association.objects.filter(table2=table)
        fields = Field.objects.filter(table=table)
    ctxt = {
        'table': table,
        'schema': schema,
        'associations': associations,
        'fields': fields,
        'isNew': isNew
    }
    res = render(req, 'dummydatabases/editTable.html', ctxt)
    res.set_cookie('currentTable', table.id)
    return res

@login_required(login_url='/login')
def removeTable(req):
    table = Table.objects.get(id=int(req.POST.get('tableId')))
    table.delete()
    res = redirect('/editSchema')
    return res

@login_required(login_url='/login')
def saveTable(req):
    table = Table.objects.get(id=int(req.COOKIES.get('currentTable')))
    table.schema = Schema.objects.get(id=int(req.COOKIES.get('currentSchema')))
    table.name = req.POST.get('name')
    table.rowCount = req.POST.get('rowCount')
    table.save()
    res = redirect('/editSchema')
    return res

# FIELD CRUD ------------------------------------------------------------------------------------------

@login_required(login_url='/login')
def editField(req):
    table = Table.objects.get(id=int(req.COOKIES.get('currentTable')))
    if req.POST.get('isNew') == 'true':
        field = Field()
        field.name = 'field1'
        field.table = table
        field.save()
    elif req.POST.get('isNew') == 'false':
        field = Field.objects.get(id=int(req.POST.get('fieldId')))
    options = field.options
    for k, v in options.items():
        if k == 'includeTime':
            options['minDate'] = datetime.strftime(datetime.fromtimestamp(options['minDate']), '%Y-%m-%d')
            options['maxDate'] = datetime.strftime(datetime.fromtimestamp(options['maxDate']), '%Y-%m-%d')
            break
    ctxt = {
        'table': table,
        'field': field,
        'types': Field.dataTypes.items(),
        'fieldOptions': options
    }
    res = render(req, 'dummydatabases/editField.html', ctxt)
    return res

@login_required(login_url='/login')
def removeField(req):
    field = Field.objects.get(id=int(req.POST.get('fieldId')))
    field.delete()
    return editTable(req)

@login_required(login_url='/login')
def saveField(req):
    field = Field.objects.get(id=int(req.POST.get('fieldId')))
    field.table = Table.objects.get(id=int(req.COOKIES.get('currentTable')))
    field.name = req.POST.get('name')
    field.dataType = req.POST.get('dataType')
    field.options = getFieldOptions(req.POST.get('dataType'), req.POST)
    field.save()
    return editTable(req)

# ASSOCIATION CRUD ------------------------------------------------------------------------------------------

@login_required(login_url='/login')
def editAssociation(req):
    if req.POST.get('isNew') == 'true':
        table = Table.objects.get(id=int(req.POST.get('tableId')))
        association = Association()
        association.table1 = table
        association.save()
    elif req.POST.get('isNew') == 'false':
        association = Association.objects.get(id=int(req.POST.get('associationId')))
        table = association.table1
    ctxt = {
        'table': table,
        'association': association,
        'types': Association.types.items(),
        'tables': Table.objects.filter(schema=table.schema).exclude(id=table.id)
    }
    res = render(req, 'dummydatabases/editAssociation.html', ctxt)
    res.set_cookie('currentTable', table.id)
    return res

@login_required(login_url='/login')
def removeAssociation(req):
    association = Association.objects.get(id=int(req.POST.get('associationId')))
    association.delete()
    res = redirect('/editTable')
    return res

@login_required(login_url='/login')
def saveAssociation(req):
    association = Association.objects.get(id=int(req.POST.get('associationId')))
    association.table1 = Table.objects.get(id=int(req.COOKIES.get('currentTable')))
    association.table2 = Table.objects.get(id=int(req.POST.get('table2')))
    association.type = Association.types.get(int(req.POST.get('type')))
    if req.POST.get('type') == 'many to many':
        association.rowCount = int(req.POST.get('rowCount'))
    association.save()
    res = redirect('/editTable')
    return res

# DATABASE/DATA GENERATION ------------------------------------------------------------------------------------------

@login_required(login_url='/login')
def downloadView(req):
    schema = Schema.objects.get(id=int(req.POST.get('schemaId')))
    ctxt = {
        'schema': schema
    }
    res = render(req, 'dummydatabases/downloadOptions.html', ctxt)
    return res

def downloadFile(path):
    filePath = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(filePath):
        with open(filePath, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filePath)
            return response
    raise Http404

def deleteFile(path):
    filePath = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(filePath):
        os.remove(filePath)

# orders tables in a consumable manner for the sql to execute properly

def getOrderedTableList(schema):
    tables = []
    for table in Table.objects.filter(schema=schema):
        association = Association.objects.exclude(type='many to many').filter(table2=table)
        if len(association):
            tables.append(table)
        else:
            tables.insert(0, table)
    return tables

@login_required(login_url='/login')
def generateDatabase(req):
    schema = Schema.objects.get(id=int(req.POST.get('schemaId')))
    tableData = {}
    for table in getOrderedTableList(schema):
        tableData.update({table.name: genTableData(table)})
    dbType = req.POST.get('dbType')
    fileType = req.POST.get('fileType')
    match dbType:
        case 'MONGODB':
            fileExtension = ''
        case 'MYSQL':
            fileExtension = ''
        case 'POSTGRESQL':
            fileExtension = 'sql'
        case 'SQLITE':
            fileExtension = fileType
        case _:
            fileExtension = 'sqlite3'
    filePath = f'{schema.name}.{fileExtension}'
    generateFile(schema, tableData, dbType, fileType)
    res = downloadFile(filePath)
    deleteFile(filePath)
    return res

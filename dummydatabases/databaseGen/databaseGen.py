
from .mongoGen import generateMongodbFile
from .mysqlGen import generateMysqlFile
from .pgGen import generatePgFile
from .sqliteGen import generateSqliteFile

def generateFile(schema, tableData, dbType, fileType):
    if dbType ==  'MONGODB':
        generateMongodbFile(schema, tableData)
    elif dbType ==  'MYSQL':
        generateMysqlFile(schema, tableData)
    elif dbType ==  'POSTGRESQL':
        generatePgFile(schema, tableData)
    elif dbType ==  'SQLITE':
        generateSqliteFile(schema, tableData, fileType)

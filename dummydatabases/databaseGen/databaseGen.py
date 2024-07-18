
from .mongoGen import generateMongodbFile
from .mysqlGen import generateMysqlFile
from .pgGen import generatePgFile
from .sqliteGen import generateSqliteFile

def generateFile(schema, tableData, dbType, fileType):
    match dbType:
        case 'MONGODB':
            generateMongodbFile(schema, tableData)
        case 'MYSQL':
            generateMysqlFile(schema, tableData)
        case 'POSTGRESQL':
            generatePgFile(schema, tableData)
        case 'SQLITE':
            generateSqliteFile(schema, tableData, fileType)

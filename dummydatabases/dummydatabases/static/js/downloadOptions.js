
// CONSTANTS
const dbTypeEl = document.querySelector('#dbType');
const mongoDbInstructionsEl = document.querySelector('#mongoDbInstructions');
const mysqlInstructionsEl = document.querySelector('#mysqlInstructions');
const postgresqlInstructionsEl = document.querySelector('#postgresqlInstructions');
const sqliteInstructionsEl = document.querySelector('#sqliteInstructions');
const sqliteOptionsEl = document.querySelector('#sqliteOptions');

dbTypeEl.onchange = () => {
    switch (dbTypeEl.value) {
        case 'MONGODB':
            mongoDbInstructionsEl.style = '';
            mysqlInstructionsEl.style.display = 'none';
            postgresqlInstructionsEl.style.display = 'none';
            sqliteInstructionsEl.style.display = 'none';
            sqliteOptionsEl.style.display = 'none';
            break;
        case 'MYSQL':
            mongoDbInstructionsEl.style.display = 'none';
            mysqlInstructionsEl.style = '';
            postgresqlInstructionsEl.style.display = 'none';
            sqliteInstructionsEl.style.display = 'none';
            sqliteOptionsEl.style.display = 'none';
            break;
        case 'POSTGRESQL':
            mongoDbInstructionsEl.style.display = 'none';
            mysqlInstructionsEl.style.display = 'none';
            postgresqlInstructionsEl.style = '';
            sqliteInstructionsEl.style.display = 'none';
            sqliteOptionsEl.style.display = 'none';
            break;
        case 'SQLITE':
            mongoDbInstructionsEl.style.display = 'none';
            mysqlInstructionsEl.style.display = 'none';
            postgresqlInstructionsEl.style.display = 'none';
            sqliteInstructionsEl.style = '';
            sqliteOptionsEl.style = '';
            break;
        default:
            mongoDbInstructionsEl.style.display = 'none';
            mysqlInstructionsEl.style.display = 'none';
            postgresqlInstructionsEl.style.display = 'none';
            sqliteInstructionsEl.style.display = 'none';
            sqliteOptionsEl.style.display = 'none';
            break;
    }
}

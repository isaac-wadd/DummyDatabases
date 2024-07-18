
const fieldTypesEl = document.querySelector('#fieldTypes');
const stringRandomOptions = document.querySelector('#stringRandomOptions');
const intOptionsEl = document.querySelector('#intOptions');
const floatOptionsEl = document.querySelector('#floatOptions');
const dateTimeOptionsEl = document.querySelector('#dateTimeOptions');
const stringDataOptionsEl = document.querySelector('#stringDataOptions');
const stringDataOptions = document.querySelector('#stringOptions');
const allStringDataOptionsEls = document.querySelectorAll('.strOptions');

function hideAllStringDataOptionsEls() {
    stringDataOptions.style.display = 'none';
    allStringDataOptionsEls.forEach((el) => {
        el.style.display = 'none';
    });
}

function showStringDataOptionsEl() {
    stringDataOptions.style = '';
    let optionsElId = '#' + stringDataOptionsEl.value + 'Options';
    let optionsEl = document.querySelector(optionsElId);
    optionsEl.style = '';
    let allOtherOptionsEls = document.querySelectorAll('.strOptions:not(' + optionsElId + ')');
    allOtherOptionsEls.forEach((el) => {
        el.style.display = 'none';
    });
}

// changes visibility of options based on field type

fieldTypesEl.onchange = () => {
    switch (fieldTypesEl.value) {
        case 'TEXT':
            stringDataOptionsEl.value == 'random' ? stringRandomOptions.style = '' : stringRandomOptions.style.display = 'none';
            intOptionsEl.style.display = 'none';
            floatOptionsEl.style.display = 'none';
            dateTimeOptionsEl.style.display = 'none';
            stringDataOptionsEl.style = '';
            showStringDataOptionsEl();
            return;
        case 'INTEGER':
            stringRandomOptions.style.display = 'none';
            intOptionsEl.style = '';
            floatOptionsEl.style.display = 'none';
            dateTimeOptionsEl.style.display = 'none';
            stringDataOptionsEl.style.display = 'none';
            hideAllStringDataOptionsEls();
            break;
        case 'REAL':
            stringRandomOptions.style.display = 'none';
            intOptionsEl.style.display = 'none';
            floatOptionsEl.style = '';
            dateTimeOptionsEl.style.display = 'none';
            stringDataOptionsEl.style.display = 'none';
            hideAllStringDataOptionsEls();
            break;
        case 'DATETIME':
            stringRandomOptions.style.display = 'none';
            intOptionsEl.style.display = 'none';
            floatOptionsEl.style.display = 'none';
            dateTimeOptionsEl.style = '';
            stringDataOptionsEl.style.display = 'none';
            hideAllStringDataOptionsEls();
            break;
        default:
            stringRandomOptions.style.display = 'none';
            intOptionsEl.style.display = 'none';
            floatOptionsEl.style.display = 'none';
            dateTimeOptionsEl.style.display = 'none';
            stringDataOptionsEl.style.display = 'none';
            hideAllStringDataOptionsEls();
            break;
    }
}

// changes visibility of options based on string data choice

stringDataOptionsEl.onchange = () => { showStringDataOptionsEl(); }

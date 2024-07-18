
// CONSTANTS
const numberEl = document.querySelector('#numberEl');
const associationTypeEl = document.querySelector('#type');

associationTypeEl.onchange = () => {
    switch (associationTypeEl.value) {
        case '3':
            numberEl.style = '';
            break;
        default:
            numberEl.style.display = 'none';
            break;
    }
}

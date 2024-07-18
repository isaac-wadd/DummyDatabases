
const pageTitle = document.querySelector('title').innerText;
const allBtns = document.querySelectorAll('button');

function confirmAction(btn, form, e) {
    if (form == backBtnForm) {
        let accepted = confirm('Changes will not be saved. Are you sure?');
        if (accepted) {
            form.submit();
        }
        else {
            e.preventDefault();
        }
    }
    else if (btn.className.includes('deleteBtn')) {
        let accepted = confirm('This will delete the table entirely. Are you sure you want to do this? (You cannot undo this action!)');
        if (accepted) {
            form.submit();
        }
        else {
            e.preventDefault();
        }
    }
}

allBtns.forEach((btn) => {
    btn.onclick = (e) => {
        confirmAction(btn, btn.parentElement, e);
    }
});

const isComm = document.querySelector("input[name=is_commercial]");
const comm_type = document.getElementById('commercial_type');
const size_in_sqm = document.getElementById('size_in_sqm');

const disableRentPer = () => {
    const inline_form = document.getElementsByClassName('inline-form-field');
    if(!inline_form) return;

    for (let el of inline_form){
        el.classList.add('row')
        const per = el.querySelector('select')
        per.disabled = !isComm.checked;
    }
}

if (!isComm.checked){
    comm_type.disabled = !isComm.checked;
    size_in_sqm.disabled = !isComm.checked;
}

isComm.addEventListener('change', (el) => {
    comm_type.disabled = !isComm.checked;
    size_in_sqm.disabled = !isComm.checked;
    disableRentPer()
});

const inline_form_list = document.getElementsByClassName('inline-field-list')[0]
inline_form_list.addEventListener("DOMNodeInserted", (el) => {
    disableRentPer();
})
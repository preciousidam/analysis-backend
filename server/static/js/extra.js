const isComm = document.querySelector("input[name=is_commercial]");
const comm_type = document.getElementById('commercial_type');
const size_in_sqm = document.getElementById('size_in_sqm');
const rent_per_sqm = document.getElementById('rent_per_sqm');

if (!isComm.checked){
    comm_type.disabled = !isComm.checked;
    size_in_sqm.disabled = !isComm.checked;
    rent_per_sqm.disabled = !isComm.checked;
}

isComm.addEventListener('change', (el) => {
    comm_type.disabled = !isComm.checked;
    size_in_sqm.disabled = !isComm.checked;
    rent_per_sqm.disabled = !isComm.checked;
})
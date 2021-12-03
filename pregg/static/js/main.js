// Check answers to questions
let g = 0;
let h = 0;
let r = 0;
let s = 0;

function gryffindor(event) {
    let button = event.target;
    button.style.backgroundColor = 'Purple';
    g += 1;
}

function hufflepuff(event) {
    let button = event.target;
    button.style.backgroundColor = 'Green';
    h += 1;
}

function ravenclaw(event) {
    let button = event.target;
    button.style.backgroundColor = 'Green';
    r += 1;
}

function slytherin(event) {
    let button = event.target;
    button.style.backgroundColor = 'Green';
    s += 1;
}

function checkMC(event) {
    let button = event.target;
    if (button.innerHTML == 'Four') {
        button.style.backgroundColor = 'Green';
        button.parentElement.querySelector('.feedback').innerHTML = "Correct!";
    }
    else {
        button.style.backgroundColor = 'Red';
        button.parentElement.querySelector('.feedback').innerHTML = 'Incorrect';
    }
}

function checkFR(event) {
    let button = event.target;
    let input = button.parentElement.querySelector('input');
    if (input.value === 'BTS') {
        input.style.backgroundColor = 'Green';
        input.parentElement.querySelector('.feedback').innerHTML = 'Correct!';
    }
    else {
        input.style.backgroundColor = 'Red';
        input.parentElement.querySelector('.feedback').innerHTML = 'Incorrect';
    }
}
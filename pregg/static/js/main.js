// Check answers to questions
let g = 0;
let h = 0;
let r = 0;
let s = 0;
let count = 0;
let result = document.getElementById("result");

function gryffindor(event) {
    let button = event.target;
    button.style.backgroundColor = 'lightsteelblue';
    g += 1;
    count += 1;
}

function hufflepuff(event) {
    let button = event.target;
    button.style.backgroundColor = 'lightsteelblue';
    h += 1;
    count += 1;
}

function ravenclaw(event) {
    let button = event.target;
    button.style.backgroundColor = 'lightsteelblue';
    r += 1;
    count += 1;
}

function slytherin(event) {
    let button = event.target;
    button.style.backgroundColor = 'lightsteelblue';
    s += 1;
    count += 1;
}

function button1(){
    document.querySelectorAll('.button1').forEach(el => el.setAttribute('disabled', true)); 
    if (count >= 5)
    {
        updateResult();
    }
}

function button2(){
    document.querySelectorAll('.button2').forEach(el => el.setAttribute('disabled', true)); 
    if (count >= 5)
    {
        updateResult();
    }
}

function button3(){
    document.querySelectorAll('.button3').forEach(el => el.setAttribute('disabled', true)); 
    if (count >= 5)
    {
        updateResult();
    }
}

function button4(){
    document.querySelectorAll('.button4').forEach(el => el.setAttribute('disabled', true)); 
    if (count >= 5)
    {
        updateResult();
    }
}

function button5(){
    document.querySelectorAll('.button5').forEach(el => el.setAttribute('disabled', true)); 
    if (count >= 5)
    {
        updateResult();
    }
}

function updateResult(){
    if (g >= 2){
        result.innerHTML = "Your baby will be a... Gryffindor! They will be brave, stand up for their friends, and always stick to what they think is right.";
    }
    else if (h >= 2){
        result.innerHTML = "Your baby will be a... Hufflepuff! They will be a caring friend, a good listener, and always see the good in people.";
    }
    else if (r >= 2){
        result.innerHTML = "Your baby will be a... Ravenclaw! They will be studious, good at reading the situation, and always have good solutions to problems.";
    }
    else if (s >= 2){
        result.innerHTML = "Your baby will be a Slytherin! They will be opportunistic, crafty, and maybe have green as their favorite color.";
    }
}
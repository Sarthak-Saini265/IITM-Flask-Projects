let lyr = document.getElementById('lyrics');
let lyr_div = document.getElementById('lyrics_div')
let overlay = document.getElementById('overlay')
// console.log(lyr)
// console.log(lyr_div.style.display)

function lyrics() {
    if (lyr_div.style.display === 'none' || lyr_div.style.display === '') {
        lyr_div.style.display = 'block';
        overlay.style.display = 'block';
    } else {
        lyr_div.style.display = 'none';
        overlay.style.display = 'none';
    }
}

lyr.addEventListener('click', lyrics);



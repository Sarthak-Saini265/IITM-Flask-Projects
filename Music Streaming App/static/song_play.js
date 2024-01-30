let buttons = document.getElementsByClassName('song_play');
// let pause_buttons = document.getElementsByClassName('song_pause');
let audio = new Audio();
// console.log('Script Loaded')

let l = []
function play(event) {
    console.log('Button clicked:', event.currentTarget);
    let path = event.currentTarget.getAttribute('data-mp3');
    l.push(path)
    console.log(l)
    console.log('MP3 path:', path);
    if (l.length < 2 || l[l.length - 1] != l[l.length - 2]) {
        audio.src = '/static' + path;
        audio.play()
        for (let i = 0; i < buttons.length; i++) {
            buttons[i].innerHTML = '▶';
            buttons[i].style.padding = '11px';
            buttons[i].style.paddingRight = '6px';
            buttons[i].style.fontSize = '27px'
        }
        event.currentTarget.innerHTML = '▐▐'
        event.currentTarget.style.paddingRight = '15px';
        event.currentTarget.style.fontSize = '19px'
        event.currentTarget.style.paddingBottom = '10px';
    }
    else {
        if (!audio.paused) {
            audio.pause();
            event.currentTarget.innerHTML = '▶'
            event.currentTarget.style.padding = '11px';
            event.currentTarget.style.paddingRight = '6px';
            event.currentTarget.style.fontSize = '27px'
        }
        else {
            audio.play()
            event.currentTarget.innerHTML = '▐▐'
            event.currentTarget.style.paddingRight = '15px';
            event.currentTarget.style.fontSize = '19px'
            event.currentTarget.style.paddingBottom = '10px';
        }
    }
}



for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', play);
    //    pause_buttons[i].addEventListener('click', pause)
}



// document.addEventListener('click', function(event) {
//     if (event.target.classList.contains('song_play')) {
//         play(event);
//     }
// });


// console.log('jnwjndjwandwjndjwn')


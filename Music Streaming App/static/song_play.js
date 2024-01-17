let buttons = document.getElementsByClassName('song_play');
let pause_buttons = document.getElementsByClassName('song_pause');
let audio = new Audio();
console.log('Script Loaded')

function play(event) {
    console.log('Button clicked:', event.currentTarget);
    let path = event.currentTarget.getAttribute('data-mp3');
    console.log('MP3 path:', path);
    if (!audio.paused) {
        audio.src = '/static' + path;
    }

    audio.play();
}

function pause(event) {
    console.log('Pause button clicked:', event.currentTarget);
    audio.pause();
  }

for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', play);
    pause_buttons[i].addEventListener('click', pause)
}



// document.addEventListener('click', function(event) {
//     if (event.target.classList.contains('song_play')) {
//         play(event);
//     }
// });


// console.log('jnwjndjwandwjndjwn')


let buttons = document.getElementsByClassName('song_play');
let audio = new Audio();

function play(event) {
    console.log('Button clicked:', event.currentTarget);
    let path = event.currentTarget.getAttribute('data-mp3');
    console.log('MP3 path:', path);
    audio.src = '/static' + path;
    audio.play();
}

for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', play);
}

document.addEventListener('click', function(event) {
    if (event.target.classList.contains('song_play')) {
        play(event);
    }
});


// console.log('jnwjndjwandwjndjwn')


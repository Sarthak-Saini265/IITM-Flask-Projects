let buttons = document.getElementsByClassName('song_play');
let bar_sname = document.getElementById('name-song')
let play_button = document.getElementById('play_button')
let artist_name = document.getElementById('artist_name')
// let pause_buttons = document.getElementsByClassName('song_pause');
let audio = new Audio();
let isPlaying = false;
// console.log('Script Loaded')

function playPause() {
    if (audio.paused) {
        audio.play();
        play_button.innerHTML = '▐▐';
    } else {
        audio.pause();
        play_button.innerHTML = '▶';
    }
}

play_button.addEventListener('click', playPause);

function play(event) {
    let path = event.currentTarget.getAttribute('data-mp3');
    let name = event.currentTarget.getAttribute('name-mp3');
    let artist = event.currentTarget.getAttribute('artist-mp3');
    audio.src = '/static' + path;
    bar_sname.innerHTML = name;
    artist_name.innerHTML = artist;

    // Pause if currently playing the same song
    if (!audio.paused && audio.src === audio.src) {
        audio.pause();
        play_button.innerHTML = '▶';
    } else {
        audio.play();
        play_button.innerHTML = '▐▐';
    }
}

for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', play);
}




// let l = []
// function play(event) {
//     console.log('Button clicked:', event.currentTarget);
//     let path = event.currentTarget.getAttribute('data-mp3');
//     let name = event.currentTarget.getAttribute('name-mp3')
//     l.push(path)
//     console.log(l)
//     console.log('MP3 path:', path);
//     if (l.length < 2 || l[l.length - 1] != l[l.length - 2]) {
//         audio.src = '/static' + path;
//         bar_sname.innerHTML = name
//         audio.play()
//         // for (let i = 0; i < buttons.length; i++) {
//         //     // buttons[i].innerHTML = '▶';
//         //     // buttons[i].style.padding = '11px';
//         //     // buttons[i].style.paddingRight = '6px';
//         //     // buttons[i].style.fontSize = '27px'
//         // }
//         play_button.innerHTML = "▐▐"
//         // event.currentTarget.innerHTML = '▐▐'
//         // event.currentTarget.style.paddingRight = '15px';
//         // event.currentTarget.style.fontSize = '19px'
//         // event.currentTarget.style.paddingBottom = '10px';
//     }
//     else {
//         if (!audio.paused) {
//             audio.pause();
//             play_button.innerHTML = '▶'
//             // event.currentTarget.innerHTML = '▶'
//             // event.currentTarget.style.padding = '11px';
//             // event.currentTarget.style.paddingRight = '6px';
//             // event.currentTarget.style.fontSize = '27px'
//         }
//         else {
//             audio.play()
//             play_button.innerHTML = '▐▐'
//             // event.currentTarget.innerHTML = '▐▐'
//             // event.currentTarget.style.paddingRight = '15px';
//             // event.currentTarget.style.fontSize = '19px'
//             // event.currentTarget.style.paddingBottom = '10px';
//         }
//     }
// }



// for (let i = 0; i < buttons.length; i++) {
//     buttons[i].addEventListener('click', play);
//     //    pause_buttons[i].addEventListener('click', pause)
// }



// document.addEventListener('click', function(event) {
//     if (event.target.classList.contains('song_play')) {
//         play(event);
//     }
// });


// console.log('jnwjndjwandwjndjwn')


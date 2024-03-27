let all_songs_div = document.getElementsByClassName('all_songs');
let all_albums_div = document.getElementsByClassName('all_albums');
let songs_divs = document.getElementsByClassName('songs');
let albums_divs = document.getElementsByClassName('albums');
let songs_heading = document.getElementsByClassName('search_songs');
let albums_heading = document.getElementsByClassName('search_albums');
let nothing_found = document.getElementsByClassName('nothing_found');

console.log('all_songs' + songs_divs.length)
console.log('all_albums' + albums_divs.length)
console.log('all_albums_div' + all_albums_div.length)


if (songs_divs.length == 0 && albums_divs.length == 0) {
    all_albums_div[0].style.display = 'none';
    songs_heading[0].style.display = 'none';
    all_songs_div[0].style.display = 'none';
    albums_heading[0].style.display = 'none';
    nothing_found[0].style.display = 'block';
} else {
    if (songs_divs.length != 0 && albums_divs.length != 0) {
        all_albums_div[0].style.display = 'flex';
        songs_heading[0].style.display = 'block';
        all_songs_div[0].style.display = 'flex';
        albums_heading[0].style.display = 'block';
        nothing_found[0].style.display = 'none';
    } else if (songs_divs.length == 0 && albums_divs.length != 0) {
        nothing_found[0].style.display = 'none';
        songs_heading[0].style.display = 'none';
        all_songs_div[0].style.display = 'none';
    } else if (albums_divs.length == 0 && songs_divs.length != 0) {
        nothing_found[0].style.display = 'none';
        albums_heading[0].style.display = 'none';
        all_albums_div[0].style.display = 'none';
    }
}




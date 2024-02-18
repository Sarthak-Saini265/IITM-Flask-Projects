let s_name = document.getElementsByClassName('song_h3')

for (let i = 0; i < s_name.length; i++) {
    let sliced = s_name[i].textContent.slice(0,16)
    s_name[i].innerHTML = sliced + "..."
    console.log(sliced)
    console.log(s_name[i])
}


// console.log(s_name)


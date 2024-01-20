function handleRatingChange(selectElement, songPath, song_id, username) {
    var selectedValue = selectElement.value;
    selectedValue = parseInt(selectedValue)
    console.log(typeof(selectedValue))
    console.log(selectedValue)
    if (selectedValue !== "select") {
        window.location.href = `/${username}/song/${song_id}/rating/${selectedValue}`;
        console.log("Selected Rating: " + selectedValue + " for song: " + songPath);
    }
}



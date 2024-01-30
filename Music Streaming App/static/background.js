document.addEventListener('DOMContentLoaded', function () {
    const songs = document.querySelectorAll('.songs');
    
    songs.forEach(song => {
        song.addEventListener('mouseover', function () {
            const content = this.closest('.main_div').querySelector('.content');
            content.style.backgroundImage = 'linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.7)), url(/static/user_page_test_1.jpg)';
        });

        song.addEventListener('mouseout', function () {
            const content = this.closest('.main_div').querySelector('.content');
            content.style.backgroundImage = 'linear-gradient(rgba(0, 0, 0, 0.95), rgba(0, 0, 0, 0.95)), url(/static/user_page_test_1.jpg)';
        });
    });
});
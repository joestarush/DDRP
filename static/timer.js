document.addEventListener("DOMContentLoaded", function() {
    let timerElement = document.getElementById('timer');
    let time = 180;

    setInterval(function() {
        let minutes = Math.floor(time / 60);
        let seconds = time % 60;
        timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        if (time > 0) {
            time--;
        }
    }, 1000);
});

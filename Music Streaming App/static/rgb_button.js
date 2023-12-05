let currentColorIndex = 0;
const colors = [
    [255, 0, 0],   // Red
    [255, 255, 0], // Yellow
    [0, 255, 0],   // Green
    [0, 255, 255], // Cyan
    [0, 0, 255],   // Blue
    [255, 0, 255]  // Magenta
];

function changeBorderColor() {
    const button = document.getElementById('signin_logo');
    currentColorIndex = (currentColorIndex + 1) % colors.length;
    const [r, g, b] = colors[currentColorIndex];
    button.style.border = `2px solid rgb(${r}, ${g}, ${b})`;
}
// FastAPI Static Files Demo - JavaScript

console.log('JavaScript file loaded successfully from /static/script.js! 🎉');

document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('testButton');
    const output = document.getElementById('output');
    
    let clickCount = 0;
    
    button.addEventListener('click', function() {
        clickCount++;
        output.textContent = `Button clicked ${clickCount} time${clickCount !== 1 ? 's' : ''}! JavaScript is working! ✨`;
        
        // Add a little animation
        output.style.transform = 'scale(1.1)';
        setTimeout(() => {
            output.style.transform = 'scale(1)';
        }, 200);
    });
    
    // Log that everything is ready
    console.log('Event listeners attached. Try clicking the button!');
});

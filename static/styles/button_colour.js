// Get all elements with the class 'recipe__container'
var recipeContainers = document.querySelectorAll('.recipe__container');

// Add a click event listener to each 'recipe__container' element
recipeContainers.forEach(function (container) {
    container.addEventListener('click', function () {
        // Toggle the 'clicked' class on the clicked element
        if (container.classList.contains('clicked')) {
            container.classList.remove('clicked');
        } else {
            container.classList.add('clicked');
        }
    });
});


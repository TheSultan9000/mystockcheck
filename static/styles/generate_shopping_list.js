// Get all elements with the class '.recipe__container'
var selectionElements = document.querySelectorAll('.recipe__container');

// Initialize an array to store selected items
var selectedItems = [];

// Add the click event listener to all '.recipe__container' elements
selectionElements.forEach(function (element) {
    element.addEventListener('click', handleContainerClick);
});

// Create an event listener function
function handleContainerClick(event) {
    var clickedContainer = findParentContainer(event.target, 'recipe__container');

    if (clickedContainer) {
        // Check if the clicked element has the 'clicked' class
        if (clickedContainer.classList.contains('clicked')) {
            // Extract the entire content of the container
            var containerContent = clickedContainer.textContent;

            // Add the selection data to the array
            selectedItems.push(containerContent);
        } else {
            // Extract the entire content of the container
            var containerContent = clickedContainer.textContent;

            // Find the index of the containerContent in the selectedItems array
            var removeIndex = selectedItems.indexOf(containerContent);

            // Check if the value exists in the array before removing
            if (removeIndex !== -1) {
                selectedItems.splice(removeIndex, 1);
            }
        }

        // Call sendSelectedItems() whenever a .recipe__container is clicked
        sendSelectedItems();
    }
}

// Function to find the nearest ancestor with a specific class
function findParentContainer(element, className) {
    while (element && !element.classList.contains(className)) {
        element = element.parentNode;
    }
    return element;
}

// Function to send selected items in a POST request
function sendSelectedItems() {
    var formData = new FormData();
    formData.append('selectedItems', JSON.stringify(selectedItems));

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


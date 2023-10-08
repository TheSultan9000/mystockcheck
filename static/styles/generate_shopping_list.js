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
    var clickedContainer = event.target;

    // Check if the clicked element has the 'clicked' class
    if (clickedContainer.classList.contains('clicked')) {
        // Get the index of the clicked element in the NodeList
        var index = Array.from(selectionElements).indexOf(clickedContainer);

        // Extract the ingredient and quantity from the corresponding elements
        var selectionVar = selectionElements[index].textContent;

        // Add the selection data to the array
        selectedItems.push(selectionVar);
    } else {
        // Get the index of the clicked element in the NodeList
        var index = Array.from(selectionElements).indexOf(clickedContainer);

        // Extract the ingredient and quantity from the corresponding elements
        var selectionVar = selectionElements[index].textContent;

        // Find the index of the selectionVar in the selectedItems array
        var removeIndex = selectedItems.indexOf(selectionVar);

        // Check if the value exists in the array before removing
        if (removeIndex !== -1) {
            selectedItems.splice(removeIndex, 1);
        }
    }

    // Call sendSelectedItems() whenever a .recipe__container is clicked
    sendSelectedItems();
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

